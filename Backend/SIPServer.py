import asyncio
from autobahn.asyncio.websocket import WebSocketServerFactory
from autobahn.asyncio.websocket import WebSocketServerProtocol
from sip_parser.exceptions import SipParseError
from sip_parser.sip_message import SipMessage
import requests

SIP_SERVER_IP = "127.0.0.1"
SIP_SERVER_PORT = '5001'
# API connection used for user auth
API_PREFIX = 'http://'
API_IP = '127.0.0.1'
API_PORT = '5000'
API_URL = API_PREFIX + API_IP + ':' + API_PORT

debugMode = True
# holds all currently authorized sockets
# key is user_id value dict with sip_username,call_id
sip_users = {}


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
        if debugMode: print("Autorizing user!")
        if 'cookie' not in request.headers:
            if debugMode: print("Missing cookie!")
            self.sendHttpErrorResponse(401, "Unauthorized")
            return
        # send auth cookie over to API for verification
        headers = {
            'orgin': "http://" + SIP_SERVER_IP + ":" + SIP_SERVER_PORT,
            'cookie': request.headers['cookie']
        }
        r = requests.get(url=API_URL + '/user/check_auth', headers=headers)
        response = r.json()

        if response is None or response['result'] != 'True':
            if debugMode: print("Authorization failed!")
            self.sendHttpErrorResponse(401, "Unauthorized")
            return

        if debugMode: print("Authorization succesfull!")


    def onOpen(self):
        if debugMode: print("Connection Opened!")

    # TODO
    def on_register(self, msg):
        print(msg)

        # send back succesfull register message
        # resp.method = 'REGISTER'
        # self.sendData(resp)

    # TODO
    def on_invite(self, msg):
        print(msg)
        # send invite to invited person
        # handle person not connected

    def onMessage(self, payload, isBinary):
        msg = payload.decode('utf8')
        if debugMode: print("New message")
        if debugMode: print(msg)

        if len(msg) == 0:
            return

        # parse msg into managable format
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
    factory = WebSocketServerFactory()
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
