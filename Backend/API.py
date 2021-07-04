import json
import math

from flask import Flask, request, jsonify, make_response
import TIPDb
import random
import hashlib
from flask_cors import CORS
from ServerState import *

local_port = '3000'
sip_server_port = '5001'
domain = 'localhost:' + local_port
orgin_prefix = "http://"
allowed_domains = [domain, '127.0.0.1', '127.0.0.1:' + local_port, 'localhost', '127.0.0.1:' + sip_server_port]
# add http:// before each allowed domain to get orgin
allowed_origins = [orgin_prefix + dom for dom in allowed_domains]
debug_mode = True

# FLASK CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = 'UZYwYYgaUzN9Aq67'
app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# COOKIES CONFIG
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE='None'
)


# generates response for given data and code with appropriate headers
def generate_response(request_got, data, HTTP_code):
    origin = request_got.environ.get('HTTP_ORIGIN', 'default value')

    if origin in allowed_origins:
        resp = make_response(jsonify(data), HTTP_code)
        resp.headers['Access-Control-Allow-Origin'] = origin
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        resp.headers['Access-Control-Allow-Methods'] = '*'
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        return resp

    return make_response({}, 400)


# LOGIN SERVICE HELPERS
def generate_session_token(user_id):
    n = random.randint(1000000000000, 9999999999999)
    n = hashlib.sha256(str(n).encode())
    return str(n.hexdigest())


def authorize_user(user_id, session_token):
    # making sure userid is a string
    user_id_str = str(user_id)
    if (user_id_str not in Sessions) or (session_token != Sessions[user_id_str]['session_token']):
        return False

    return True


@app.route('/user/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == "OPTIONS":
        return generate_response(request, {}, 200)

    request_data = request.get_json()
    if debug_mode: print("LOGIN REQUEST " + str(request_data))
    user_name = request_data['username']

    # get user data from db
    try:
        db = TIPDb.TIPDb()
        user = db.get_user(user_name)
    except Exception as ex:
        if debug_mode: ("DB ERROR" + str(ex))
        return generate_response(request, {"error": "Can't fetch from db"}, 503)

    # user wasn't found in the database - ergo wrong username
    if user is None:
        return generate_response(request, {"error": "Username doesn't exist"}, 403)

    user_id = str(user[0])
    user_pass = str(user[2])

    # actual user's password doesn't match given
    if user_pass != request_data['hashedPassword']:
        return generate_response(request, {"error": "Incorrect password"}, 403)

    # generate session and session token for user
    session_token = generate_session_token(user_id)
    Sessions[user_id] = {'session_token': session_token}

    # create cookie with session token, and send back payload with sessionToken
    resp = generate_response(request, {"userId": user_id}, 200)
    resp.set_cookie('sessionToken', session_token,
                    secure=False)  # path="user/refresh_session"
    resp.set_cookie('id', user_id,
                    secure='false')  # path="/refresh_session"
    return resp


@app.route('/user/check_auth', methods=['GET', 'OPTIONS'])
def check_auth():
    if request.method == "OPTIONS":
        return generate_response(request, {}, 200)

    # authorize user
    if 'cookie' not in request.headers:
        return generate_response(request, {"error": "Missing session token cookie."}, 401)

    # gets cookie in format key=value; key=value...
    cookies = request.headers['cookie']
    # splits into array of seperate key=value cookies
    cookies_arr = cookies.split('; ')
    # transform into dict of key:value
    cookie_dict = {}
    for cookie in cookies_arr:
        split_cookie = cookie.split('=')
        cookie_key = split_cookie[0]
        cookie_val = split_cookie[1]
        cookie_dict[cookie_key] = cookie_val

    # check for needed values
    if ('sessionToken' not in cookie_dict) or ('id' not in cookie_dict):
        return generate_response(request, {"error": "Missing session token cookie."}, 401)
    user_id = cookie_dict['id']
    result = authorize_user(user_id, cookie_dict['sessionToken'])
    return make_response({"result": str(result), 'user_id': user_id}, 200)


@app.route('/user/logout', methods=['GET', 'OPTIONS'])
def logout():
    if request.method == "OPTIONS":
        return generate_response(request, {}, 200)

    if request.args is None:
        if debug_mode: print('No player id in logout')
        return generate_response(request, {"error": "Missing playerId"}, 400)

    # check if it even contains session token cookie
    session_token = request.cookies.get('sessionToken')
    if not session_token:
        if debug_mode: print("Missing session token cookie.")
        return generate_response(request, {"error": "Missing session token cookie."}, 401)

    if debug_mode: print("LOGOUT REQUEST " + str(request.args))
    user_id = request.args['userId']

    if not authorize_user(user_id, session_token):
        return generate_response(request, {"error": "Authorisation failed."}, 401)

    # delete session token for user
    del Sessions[str(user_id)]

    # set cookie to a dummy one
    resp = generate_response(request, {"logout": 'succesfull'}, 200)
    resp.set_cookie('sessionToken', 'none',
                    secure='false')  # path="/refresh_session"
    resp.set_cookie('id', 'none',
                    secure='false')  # path="/refresh_session"
    return resp


@app.route('/user/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == "OPTIONS":
        return generate_response(request, {}, 200)

    request_data = request.get_json()
    if debug_mode: print("REGISTER REQUEST " + str(request_data))
    username = request_data['username']
    hashed_password = request_data['hashedPassword']
    email = request_data['email']

    try:
        # handle username taken
        db = TIPDb.TIPDb()
        user = db.get_user(username)
        if user is not None:
            return generate_response(request, {"error": "Username already taken"}, 403)
        user = db.get_user_by_email(username)
        if user is not None:
            return generate_response(request, {"error": "Email already in use"}, 403)
        # add to database
        db.add_user(username, hashed_password, email)
    except Exception as ex:
        if debug_mode: ("DB ERROR" + str(ex))
        return generate_response(request, {"error": "Database error"}, 503)

    return generate_response(request, {"registration": 'succesfull'}, 200)


# page_vars in format pageNumber-friendsPerPage
# ex. page_vars=7-5 requeststs 7th page of 5 friends page page
@app.route('/friends/<user_id>/<state>/<page_vars>', methods=['GET', 'OPTIONS'])
def get_friends(user_id, state, page_vars):
    if request.method == "OPTIONS":
        return generate_response(request, {}, 200)

    if (user_id is None) or (state is None):
        return generate_response(request, {'error': 'Missing arguments!'}, 400)

    if debug_mode: print("FRIEND LIST REQUEST " + str(user_id))

    # authorize user
    session_token = request.cookies.get('sessionToken')
    if not authorize_user(user_id, session_token):
        return generate_response(request, {"error": "Authorisation failed."}, 401)

    # get page number and friends per page
    friends_per_page = 10;
    page = 0;
    if page_vars is not None:
        page = int(page_vars.split('-')[0])
        friends_per_page = int(page_vars.split('-')[1])
    try:
        db = TIPDb.TIPDb()
        start = page * friends_per_page
        end = page * friends_per_page + friends_per_page
        friends = db.get_friends(user_id, state, start, end)
        friends_num = db.count_friends(user_id, state)

        data = []
        for friend in friends:
            data.append({
                'username': friend[0],
                'status': friend[1]
            })

    except Exception as ex:
        if debug_mode: ("DB ERROR" + str(ex))
        return generate_response(request, {"error": "Database error"}, 503)

    max_pages = int(friends_num / friends_per_page)
    if friends_num!=friends_per_page:
        max_pages +=1
    return generate_response(request, {'maxPages': max_pages, 'friends': json.dumps(data)}, 200)


@app.route('/friend/<action>/<user_id>/<friend_name>', methods=['POST', 'OPTIONS'])
def modify_friendship(action, user_id, friend_name):
    if request.method == "OPTIONS":
        return generate_response(request, {}, 200)

    if debug_mode: print("FRIEND REQUEST " + str(user_id) + " " + action + " " + str(friend_name))
    # authorize user
    session_token = request.cookies.get('sessionToken')
    if not authorize_user(user_id, session_token):
        return generate_response(request, {"error": "Authorisation failed."}, 401)

    try:
        db = TIPDb.TIPDb()

        # check if user exists
        friend = db.get_user(friend_name)
        if friend is None:
            # perhaps it's the email adress
            friend = db.get_user_by_email(friend_name)
            if friend is None:
                return generate_response(request, {"error": "No such user exists."}, 503)

        friend_id = friend[0]
        # cannot form friendship with self :(
        if str(friend_id) == str(user_id):
            return generate_response(request, {"error": "Befriending oneself is not that easy :("}, 400)

        are_friends = db.are_friends(user_id, friend_id)
        if len(are_friends) != 0:
            friend_status=are_friends[0][0]

        if str(action) == "invite":
            # reinvite if their friendship has been declined
            if len(are_friends) == 0 or friend_status == "DEC":
                db.invite_friend(user_id, friend_id)
                return generate_response(request, {"feedback": "Friend request sent!"}, 200)

            # handle already friends
            if  friend_status== "REQ":
                # true if user was the one to invite
                user_invited = db.did_user_invite(user_id, friend_id)

                if user_invited:
                    return generate_response(request, {"error": "Invitation already sent!"}, 400)

                db.accept_friend(friend_id, user_id)
                return generate_response(request, {"feedback": "Friend request accepted!"}, 200)

            if friend_status == "ACT":
                return generate_response(request, {"Error": "You are already friends"}, 400)

        if str(action) == "remove":
            if len(are_friends) == 0:
                return generate_response(request, {"error": "You two are not friends!"}, 503)

            # true if user was the one to invite
            user_invited = db.did_user_invite(user_id, friend_id)
            if friend_status == "REQ" and not user_invited:
                db.decline_friend(user_id, friend_id)
                return generate_response(request, {"feedback": "Friendship declined!"}, 200)

            db.remove_friends(user_id, friend_id)
            return generate_response(request, {"feedback": "Friend removed successfully!"}, 200)

    except Exception as ex:
        if debug_mode: ("DB ERROR" + str(ex))
        return generate_response(request, {"error": "Database error"}, 503)

    return generate_response(request, {"error": "Unknown error"}, 503)


# run flask app
app.run("127.0.0.1", 5000, debug=True)
