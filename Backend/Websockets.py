import asyncio
from autobahn.asyncio.websocket import WebSocketServerFactory
from autobahn.asyncio.websocket import WebSocketServerProtocol
from sip_parser.exceptions import SipParseError
from sip_parser.sip_message import SipMessage
import sip_parser
from ServerState import *

debugMode = True

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
        

    def onOpen(self):
        if debugMode: print("Connection Opened!")

    # TODO
    def on_register(self, msg:sip_parser.sip_message.SipMessage):
        print("In request:")
        # print(msg.stringify())
        # msg.add_header_from_str("ht", "hv")
        import pprint
        #pprint.pprint(msg.__dict__)
        pprint.pprint(msg.__dict__)
        msg.__dict__["method"] = "OK"
        msg.__dict__["type"] = "200"
        msg.__dict__["uri"] = ""
        msg.__dict__["headers"]["to"]["params"]["tag"] = "testtagtag"
        msg.__dict__["headers"]["supported"] = "gruu,outbound"
        print(msg.stringify())#dev

        # TODO
        # map registered address
        address = msg.__dict__["headers"]["from"]["uri"]
        sdd_pair = address.split("@")

        
        registered_users[sdd_pair[0]] = sdd_pair[1]
        print(registered_users) #dev
        print("--------------------------------") #dev

        #on success 
        #self.sendData((msg.stringify()).encode('utf-8'))

    
    def on_invite(self, msg):
        pass
        # print(msg)
        # handle person not connected
        
        # response with trying

        # send invite to invited person
        
        # get OK

        # send OK

        # get ACK

        # send ACK

        # start direct call



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
    coro = loop.create_server(factory, '127.0.0.1', 5001)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
