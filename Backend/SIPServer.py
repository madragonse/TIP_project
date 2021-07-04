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
        print("In request:")
        # print(msg.stringify())
        # msg.add_header_from_str("ht", "hv")
        #import pprint
        #pprint.pprint(msg.__dict__)
        #print(msg.stringify())#dev
        msg.__dict__["method"] = ""#dev SIP/2.0 200 OK
        msg.__dict__["uri"] = ""
        msg.__dict__["headers"]["max-forwards"] =  str(int(msg.__dict__["headers"]["max-forwards"])-1)
        msg.__dict__["headers"]["to"]["params"]["tag"] = "testtagtag"
        msg.__dict__["headers"]["supported"] = "path,gruu,outbound\r\n"
        msg.__dict__["headers"].pop('user-agent', None)

        #pprint.pprint(msg.__dict__)

        ret = "SIP/2.0 200 OK"+"\r\n"+msg.stringify()[11:-2]
        print(ret)#dev
        ret = ret.encode('utf-8')
        print(ret)


        # TODO
        # map registered address
        address = msg.__dict__["headers"]["from"]["uri"]
        sdd_pair = address.split("@")
        registered_users[sdd_pair[0]] = sdd_pair[1]


        print("--------------------------------") #dev
        #ret ='INVITE sip:user1110000000350@whatever.com SIP/2.0\r\nTo: <sip:user4110000000350@whatever.com>\r\nFroma: sip:user9990000000000@rider.com;tag=R400_BAD_REQUEST;taag=4488.1908442942.0\r\nP-Served-User: sip:user4110000000350@whatever.com\r\nCall-ID: 00000000-00001188-71C0873E-0@10.44.40.47\r\nCSeq: 1 INVITE\r\nContact: sip:user9990000000000@rider.com\r\nMax-Forwards: 70\r\nVia: SIP/2.0/TCP 10.44.40.47;branch=z9hG4bK1908442942.4488.0\r\nContent-Length: 0'
        #ret ='SIP/2.0 200 OK\r\nVia: SIP/2.0/WS rhl759du66g5.invalid;branch=z9hG4bK6861729\r\nMax-Forwards: 69\r\nTo: <sip:alice@example.com>;tag=testtagtag\r\nFrom: <sip:alice@example.com>;tag=lic5rm617m\r\nCall-ID: u5audmg3pf1rpbq5eiocni\r\nCSeq: 1 REGISTER\r\nContact: <sip:3rg0440n@rhl759du66g5.invalid;transport=ws>;+sip.ice;reg-id=1;+sip.instance="<urn:uuid:19a76f24-2edd-475c-9b8f-bccd85ceb1f2>";expires=600\r\nExpires: 600\r\nAllow: INVITE,ACK,CANCEL,BYE,UPDATE,MESSAGE,OPTIONS,REFER,INFO,NOTIFY\r\nSupported: gruu,outbound\r\nUser-Agent: JsSIP 3.8.0\r\nContent-Length: 0'
        #on success 
        self.sendMessage(payload=ret , isBinary=False)

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
