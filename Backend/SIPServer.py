import asyncio
from autobahn.asyncio.websocket import WebSocketServerFactory
from autobahn.asyncio.websocket import WebSocketServerProtocol
from sip_parser.exceptions import SipParseError
from sip_parser.sip_message import SipMessage
import requests
import pprint

from datetime import datetime, timedelta


SIP_SERVER_IP = "127.0.0.1"
SIP_SERVER_PORT = '5001'
# API connection used for user auth
API_PREFIX = 'http://'
API_IP = '127.0.0.1'
API_PORT = '5000'
API_URL = API_PREFIX + API_IP + ':' + API_PORT

debugMode = True

# holds all currently registered sockets
# key is user_id value dict with sip_username,call_id
registered_users = {}


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
        # map registered address
        registered_users[id] = {
            'username' : username,
            'registered' : (datetime.now() + timedelta(seconds=int(msg.__dict__["headers"]["expires"]))),
            'state' : None,
            'wsInstance' : self
        }

        if debugMode: print("\tRegister:")
        if debugMode: print(registered_users)

        if debugMode: print("\tResponse:")
        if debugMode: print(ret)

        ret = ret.encode('utf-8')
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
