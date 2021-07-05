from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route('/', methods=['GET'])
def home():              
    friends=[
        {'username':'test_name1', 'status':'active'},
        {'username':'test_name2', 'status':'active'},
        {'username':'test_name3', 'status':'active'},
        {'username':'test_name4', 'status':'no_active'}


    ]
    return render_template('home.html', friends=friends)