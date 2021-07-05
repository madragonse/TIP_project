import asyncio
from autobahn.asyncio.websocket import WebSocketServerFactory
from autobahn.asyncio.websocket import WebSocketServerProtocol
from sip_parser.exceptions import SipParseError
from sip_parser.sip_message import SipMessage
import requests
import pprint
from SIP.messages import get_trying, get_ok, get_ack, get_bye

from datetime import datetime, timedelta


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

    #adds new client to registered clients
    def register(self, client_id,client_name, client, expire=30):
        if client_id not in self.clients:
            self.clients[client_id] = {
                'name':client_name,
                'socket':client,
                'registered' : datetime.now() + timedelta(seconds=int(expire)),
                'state' : None,
                'mutex' : asyncio.Lock()

            }

    #deletes client from registered clients
    def unregister(self, client):
        for client_id,values in self.clients.copy().items():
            if values['socket'] == client:
                del self.clients[client_id]
                break

    #sends a msg to given clientId which is the middle part of the URI
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
        username = msg.__dict__["headers"]["from"]["name"]
        address = msg.__dict__["headers"]["from"]["uri"]
        id = address.split("@")[0].split(':')[1]

        #TODO validate registration?
        pprint.pprint(msg.__dict__)
        print(type(username))
        print(username)

        if debugMode: print("\tResponse:")
        if debugMode: print(ret)

        ret = ret.encode('utf-8')
        #save to factory for inter-client communication
        self.factory.register(id, username, self, msg.__dict__["headers"]["expires"])

        self.sendMessage(payload=ret, isBinary=False)


    def on_invite(self, msg):
        pass
        # print(msg)
        # TODO handle person not connected

        # TODO response with trying

        # TODO send invite to invited person

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
        elif sip_msg.method == "OK":
            self.on_invite(sip_msg)
        elif sip_msg.method == "ACK":
            self.on_invite(sip_msg)
        elif sip_msg.method == "TRYING":
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



