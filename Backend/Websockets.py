import asyncio
from autobahn.asyncio.websocket import WebSocketServerFactory
from autobahn.asyncio.websocket import WebSocketServerProtocol
from sip_parser.exceptions import SipParseError
from sip_parser.sip_message import SipMessage
from ServerState import *

debugMode = True


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

    def onOpen(self):
        if debugMode: print("Connection Opened!")

    # TODO
    def on_register(self, msg):
        print(msg)
        # check if is a valid username and session token

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

        #parse msg into managable format
        try:
            sip_msg = SipMessage.from_string(msg)
        except SipParseError as ex:
            print(f"Failed to parse message: {ex}")
            return

        if sip_msg.method == "REGISTER":
            self.on_register(msg)
        elif sip_msg.method == "INVITE":
            self.on_invite(msg)


if __name__ == '__main__':
    factory = WebSocketServerFactory()
    factory.headers = {
        'Sec-WebSocket-Protocol': 'sip'
    }
    factory.protocol = SIPProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', 5001)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
