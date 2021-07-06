import asyncio
import time
from autobahn.asyncio.websocket import WebSocketServerFactory
from autobahn.asyncio.websocket import WebSocketServerProtocol
import requests
from SIP.messages import *
import pprint
import re


SIP_SERVER_IP = "127.0.0.1"
SIP_SERVER_PORT = '5001'
# API connection used for user auth
API_PREFIX = 'http://'
API_IP = '127.0.0.1'
API_PORT = '5000'
API_URL = API_PREFIX + API_IP + ':' + API_PORT

debugMode = True


def getIdFromUri(uri):
    m = re.match("(sip:)(.+)@(.+)", uri)
    # in case the uri doesn't match at all
    if m is None:
        return False

    return m.group(2)


# generate uri from ID
# uri in format sip:ID@DOMANINNAME
def getUriFromId(id):
    return "sip:" + str(id) + "@" + str(SIP_SERVER_IP)


# abstraction level above protocol, used for holding all clients connected to the server
# also allows sending message to a specific client
# ex. in SIP PROTOCOL use self.factory.send_to_client(id,msg)
class InterUserCommunicationServerFactory(WebSocketServerFactory):

    def __init__(self):
        WebSocketServerFactory.__init__(self)
        # holds all currently registered sockets
        # key is user_id (middle part of URI) value dict with username and socket
        self.clients = {}
        self.SIP_VERSION = "2.0"

    #adds new client to registered clients
    def register(self, client_id,client_name, socketInstance, expire=30):
        if client_id not in self.clients:
            self.clients[client_id] = {
                'name': client_name,
                'socket': socketInstance,
                'peer_id': -1,
            }

    # deletes client from registered clients
    def unregister(self, socketInstance):
        for client_id, values in self.clients.copy().items():
            if values['socket'] == socketInstance:
                del self.clients[client_id]
                break

    # returns False if no id can be found
    def get_id_from_username(self, username):
        for client_id, values in self.clients.copy().items():
            if values['name'] == username:
                return client_id

        return False

    def get_username_from_id(self, client_id):
        if client_id not in self.clients.copy():
            return False
        return self.clients[client_id]['name']

    # returns client id by socket
    def get_id_from_socket(self, socket):
        for client_id, values in self.clients.copy().items():
            if values['socket'] == socket:
                return client_id

        return False

    def make_peers(self, first, second):
        if first not in self.clients.copy() or second not in self.clients.copy():
            return False

        self.clients[first]['peer_id'] = second
        self.clients[second]['peer_id'] = first
        return True

    def break_peers(self, first, second):
        if first not in self.clients.copy() or second not in self.clients.copy():
            return False

        self.clients[first]['peer_id'] = -1
        self.clients[second]['peer_id'] = -1
        return True

    # returns peered clients id
    def get_peer(self, socket):
        for client_id, values in self.clients.copy().items():
            if values['socket'] == socket:
                peer_id = self.clients[client_id]['peer_id']
                return peer_id

        return False

    def is_connected(self, client_id):
        return client_id in self.clients.copy()

    # sends a msg to given clientId which is the middle part of the URI
    def send_to_client(self, client_id, msg, isBinary=False):
        if client_id in self.clients.copy():
            self.clients[client_id]['socket'].sendMessage(payload=msg, isBinary=isBinary)
            return

        print("cannot find to client")


class SIPProtocol(WebSocketServerProtocol):

    def __init__(self):
        super().__init__()

    def onConnect(self, request):
        if debugMode: print("New connection!")
        if debugMode: print(request)
        # handshake_key = request.headers['sec-websocket-key']

        # check if socket wants to upgrade to SIP
        if 'sip' not in request.protocols:
            if debugMode: print("Not a SIP socket, abandoning connection!")
            return

        # authorize user
        if debugMode: print("Authorizing user!")
        if 'cookie' not in request.headers:
            if debugMode: print("Missing cookie!")
            self.failHandshake("Cannot authorize user", code=401)
            return

        headers = {
            'orgin': "http://" + SIP_SERVER_IP + ":" + SIP_SERVER_PORT,
            'cookie': request.headers['cookie']
        }

        # send auth cookie over to API for verification
        try:
            r = requests.get(url=API_URL + '/user/check_auth', headers=headers)
            response = r.json()

            if response is None or response['result'] != 'True':
                if debugMode: print("Authorization failed!")
                self.failHandshake("Cannot authorize user", code=401)
                return

            if debugMode: print("Authorization succesfull!")

        except Exception as ex:
            if debugMode: print("Cannot fetch from API")
            self.failHandshake("Cannot authorize user", code=401)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def onOpen(self):
        if debugMode: print("Connection Opened!")

    def onMessage(self, payload, isBinary):
        msg = payload.decode('utf8')
        if debugMode: print("New message--------------------------")
        if debugMode: print(type(self))
        if debugMode: print(msg)

        if len(msg) == 0:
            return

        # parse msg into manageable format
        try:
            sip_msg = SipMessage.from_string(msg)
        except SipParseError as ex:
            print(f"Failed to parse message: {ex}")
            return

        # passing to peers
        peer_id = self.factory.get_peer(self)
        if not hasattr(sip_msg, 'method'):
            if debugMode: print("No method-----------+")
            if peer_id is not False:
                self.pass_to_peer(peer_id, payload, sip_msg)

            return

        method = sip_msg.method
        if method == "REGISTER":
            self.on_register(sip_msg)
        elif method == "INVITE":
            self.on_invite(sip_msg)
        elif method == "ACK":
            self.pass_to_peer(peer_id, payload, sip_msg)
        elif method == "CANCEL" or method == "BYE":
            self.on_cancel(peer_id)

    def on_register(self, msg):
        if debugMode: print("In request:")

        # modify incoming message to make response
        msg.__dict__["method"] = ""
        msg.__dict__["uri"] = ""
        msg.__dict__["headers"]["max-forwards"] = str(int(msg.__dict__["headers"]["max-forwards"]) - 1)
        msg.__dict__["headers"]["to"]["params"]["tag"] = "testtagtag"
        msg.__dict__["headers"]["supported"] = "gruu,outbound\r\n"
        msg.__dict__["headers"]["allow"] = "INVITE,ACK,CANCEL,BYE,UPDATE"
        # delete user-agent header
        msg.__dict__["headers"].pop('user-agent', None)

        ret = "SIP/2.0 200 OK" + "\r\n" + msg.stringify()[11:-2]
        
        # TODO
        username = msg.__dict__["headers"]["from"]["name"].replace("\"", "")
        address = msg.__dict__["headers"]["from"]["uri"]
        id = getIdFromUri(address)


        if debugMode: print("\tResponse:")
        if debugMode: print(ret)

        ret = ret.encode('utf-8')
        #save to factory for inter-client communication
        self.factory.register(id, username, self, msg.__dict__["headers"]["expires"])

        self.sendMessage(payload=ret, isBinary=False)


    def on_invite(self, initial_msg):

        # get all fields into vars for ease of use
        via = initial_msg.__dict__["headers"]["via"]
        to = initial_msg.__dict__["headers"]["to"]
        from_ = initial_msg.__dict__["headers"]["from"]
        call_id = initial_msg.__dict__["headers"]["call-id"]
        cseq = initial_msg.__dict__["headers"]["cseq"]
        uri = initial_msg.__dict__["headers"]["to"]["uri"]

        """ Establish real id (original packet might have username in place of id)"""
        # establish_id returns false if user cannot be found
        invitee_id = self.establish_id(uri)
        if invitee_id is False:
            msg = get_code_msg(404, "user not found", via, from_, to, call_id, cseq)
            self.sendMessage(payload=msg.encode('utf-8'), isBinary=False)
            return

        # also get username for later use
        end_username = self.factory.get_username_from_id(invitee_id)

        """ respond to calling person with trying """
        msg = get_trying(via, from_, to, call_id, cseq)
        self.sendMessage(payload=msg.encode('utf-8'), isBinary=False)

        """ Send invite to called person """
        # swap out username in invite for actual id
        msg = initial_msg
        new_uri = getUriFromId(invitee_id)
        msg.__dict__["uri"] = new_uri
        msg.__dict__["headers"]["to"]["uri"] = new_uri
        msg.__dict__["headers"]["to"]["name"] = "\"" + str(end_username) + "\""
        msg = msg.stringify().encode('utf-8')

        """ Update user states """
        # update invitee state
        inviter_id = self.factory.get_id_from_socket(self)
        self.factory.make_peers(inviter_id, invitee_id)
        time.sleep(1)
        # send invite to the other user
        self.factory.send_to_client(invitee_id, msg)

    def establish_id(self, uri):
        # user can pass both uri or username to connect to
        # checking which one of them it is
        end_id = getIdFromUri(uri)
        # in case the ID is a username and not an ID
        possible_username = end_id.replace("\"", "")

        possible_id = self.factory.get_id_from_username(possible_username)
        if possible_id:
            end_id = possible_id

        # Handle called person not connected
        if not possible_id and not self.factory.is_connected(end_id):
            return False

        return end_id

    def pass_to_peer(self, peer_id, unedited_msg, sip_msg):
        if not peer_id:
            return

        # status = int(sip_msg.__dict__['status'])
        # if 99 < status < 200:
        #     return

        print("Passing msg to peer")
        self.factory.send_to_client(peer_id, unedited_msg)

    def on_cancel(self, peer_id):
        if not peer_id:
            return

        sock_id = self.factory.get_id_from_socket(self)
        self.factory.break_peers(peer_id, sock_id)


if __name__ == '__main__':
    ServerFactory = InterUserCommunicationServerFactory

    factory = ServerFactory()
    factory.headers = {
        'Sec-WebSocket-Protocol': 'sip'
    }
    factory.protocol = SIPProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, SIP_SERVER_IP, SIP_SERVER_PORT)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
