import asyncio
from autobahn.asyncio.websocket import WebSocketServerFactory
from autobahn.asyncio.websocket import WebSocketServerProtocol
import requests
from SIP.messages import *
import pprint

from datetime import datetime, timedelta

from SIP.utils import getIdFromUri

SIP_SERVER_IP = "127.0.0.1"
SIP_SERVER_PORT = '5001'
# API connection used for user auth
API_PREFIX = 'http://'
API_IP = '127.0.0.1'
API_PORT = '5000'
API_URL = API_PREFIX + API_IP + ':' + API_PORT

debugMode = True


# abstraction level above protocol, used for holding all clients connected to the server
# also allows sending message to a specific client
# ex. in SIP PROTOCOL use self.factory.send_to_client(id,msg)
class InterUserCommunicationServerFactory(WebSocketServerFactory):

    def __init__(self):
        WebSocketServerFactory.__init__(self)
        # holds all currently registered sockets
        # key is user_id (middle part of URI) value dict with username and socket
        self.clients = {}

    # adds new client to registered clients
    def register(self, client_id, client_name, socketInstance):
        if client_id not in self.clients:
            self.clients[client_id] = {
                'name': client_name,
                'socket': socketInstance
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

    def is_connected(self, client_id):
        return client_id in self.clients

    # sends a msg to given clientId which is the middle part of the URI
    def send_to_client(self, client_id, msg, isBinary=False):
        if client_id in self.clients:
            self.clients[client_id]['socket'].sendMessage(payload=msg, isBinary=isBinary)
            return

        print("cannot find to client")


class SIPProtocol(WebSocketServerProtocol):

    def __init__(self):
        super().__init__()
        self.SIP_VERSION = "2.0"

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

        # TODO validate registration?

        # map registered address
        # registered_users[id] = {
        #     'username' : username,
        #     'registered' : (datetime.now() + timedelta(seconds=int(msg.__dict__["headers"]["expires"]))),
        #     'state' : None,
        #     'wsInstance' : self
        # }

        # if debugMode: print("\tRegister:")
        # if debugMode: print(registered_users)

        if debugMode: print("\tResponse:")
        if debugMode: print(ret)

        ret = ret.encode('utf-8')

        # save to factory for inter-client communication
        self.factory.register(id, username, self)

        self.sendMessage(payload=ret, isBinary=False)

    # REGISTER sip:example.com SIP/2.0
    # Via: SIP/2.0/WS khlt338jf5ff.invalid;branch=z9hG4bK8153962
    # Max-Forwards: 69
    # To: <sip:alice@example.com>
    # From: <sip:alice@example.com>;tag=th6p6vvtcf
    # Call-ID: 49mgqogse7244c3ksqtdqp
    # CSeq: 84 REGISTER
    # Contact: <sip:k8vs8l68@khlt338jf5ff.invalid;transport=ws>;+sip.ice;reg-id=1;+sip.instance="<urn:uuid:24de0b00-b883-4fae-9913-2c5312a386c2>";expires=600
    # Expires: 600
    # Allow: INVITE,ACK,CANCEL,BYE,UPDATE,MESSAGE,OPTIONS,REFER,INFO,NOTIFY
    # Supported: path,gruu,outbound
    # User-Agent: JsSIP 3.8.0
    # Content-Length: 0

    def on_invite(self, msg):
        # get all fields into vars for ease of use
        via = msg.__dict__["headers"]["via"]
        to = msg.__dict__["headers"]["to"]
        from_ = msg.__dict__["headers"]["from"]
        call_id = msg.__dict__["headers"]["call-id"]
        cseq = msg.__dict__["headers"]["cseq"]
        uri = msg.__dict__["headers"]["to"]["uri"]

        """ Handle called person not connected """
        # user can pass both uri or username to connect to
        # checking which one of them it is
        id_or_username = getIdFromUri(uri)
        # assume it's the ID
        id = id_or_username
        # in case the ID is a username and not an ID
        possible_username = id_or_username.replace("\"", "")
        possible_id = self.factory.get_id_from_username(possible_username)
        if possible_id:
            id = possible_id

        if not possible_id and not self.factory.is_connected(id):
            msg = get_404_user_not_found(via, from_, to, call_id, cseq)
            self.sendMessage(payload=msg.encode('utf-8'), isBinary=False)
            return

        # TODO response with trying

        # TODO send invite to invited person

        # TODO GET NOT OK
        # 486 Busy Here – Callee is busy.

        # TODO get OK

        # TODO send OK

        # TODO get ACK

        # TODO send ACK

        # start direct call

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

        if sip_msg.method == "REGISTER":
            self.on_register(sip_msg)
        elif sip_msg.method == "INVITE":
            self.on_invite(sip_msg)


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
