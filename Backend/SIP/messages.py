from sip_parser.exceptions import SipParseError
from sip_parser.sip_message import SipMessage
import SIP.utils

#dev
# #SIP/2.0 404 the member requested is not available
# Via: SIP/2.0/UDP x.x.x.x:60000;branch=z9hG4bK1
# From: Jazz Hope<sip:jazz.hope@org1.com>;tag=5
# To: <sip:mayday@org2.com;user=ip>;tag=f6
# Call-ID: mNjdwWjkBfWrd@xx.xx.xx.xx
# CSeq: 55 INVITE
def get_404_user_not_found(via, from_, to, call_id, c_seq):
    content = {'method': ' ', 'uri': ' ',
               'headers': {"via": via, 'from': from_, 'to': to, 'call-id': call_id, 'cseq': c_seq}}

    message = SipMessage.from_dict(content)
    message = "SIP/2.0 404 User not found" + message.stringify()[11:]
    return message

def get_trying(via, from_, to, call_id, c_seq, contact=None):

    content = {'method':' ', 'uri':' ', 'headers':{"via":via, 'from':from_, 'to':to, 'call-id':call_id, 'cseq':c_seq} }
    if contact is not None: contact.append['headers']['contact'] = contact

    message = SipMessage.from_dict(content)
    message_ob = message
    message = "SIP/2.0 100 Trying"+message.stringify()[11:]
    return message, message_ob

def get_ok(via, from_, to, call_id, c_seq, contact=None):
    content = {'method':' ', 'uri':' ', 'headers':{"via":via, 'from':from_, 'to':to, 'call-id':call_id, 'cseq':c_seq} }
    if contact is not None: contact.append['headers']['contact'] = contact

    message = SipMessage.from_dict(content)
    message_ob = message
    message = "SIP/2.0 200 OK"+message.stringify()[11:]
    return message, message_ob

def get_ack(via, from_, to, call_id, c_seq, contact=None, method=' ', uri=' ', header=None):
    content = {'method':method, 'uri':uri, 'headers':{"via":via, 'from':from_, 'to':to, 'call-id':call_id, 'cseq':c_seq} }
    if contact is not None: contact.append['headers']['contact'] = contact

    message = SipMessage.from_dict(content)
    message_ob = message

    if header is not None:
        message = header+message.stringify()[11:]
    else:
        message = message.stringify()
    return message, message_ob


#dev
# ACK sip:bob@203.0.113.22:5060;transport=udp SIP/2.0
# Via: SIP/2.0/WSS df7jal23ls0d.invalid;branch=z9hG4bKhgqqp090
# Route: <sip:h7kjh12s@proxy.example.com:443;transport=ws;lr>,
#     <sip:proxy.example.com;transport=udp;lr>,
# From: sip:alice@example.com;tag=asdyka899
# To: sip:bob@example.com;tag=bmqkjhsd
# Call-ID: asidkj3ss
# CSeq: 1 ACK
# Max-Forwards: 70

#dev
# SIP/2.0 200 OK
# Via: SIP/2.0/UDP proxy.example.com;branch=z9hG4bKhjhjqw32c
#     ;received=192.0.2.10
# Via: SIP/2.0/WSS df7jal23ls0d.invalid;branch=z9hG4bK56sdasks
# Record-Route: <sip:proxy.example.com;transport=udp;lr>,
#     <sip:h7kjh12s@proxy.example.com:443;transport=ws;lr>
# From: sip:alice@example.com;tag=asdyka899
# To: sip:bob@example.com;tag=bmqkjhsd
# Call-ID: asidkj3ss
# CSeq: 1 INVITE
# Contact: <sip:bob@203.0.113.22:5060;transport=udp>
# Content-Type: application/sdp


#dev
#    SIP/2.0 100 Trying
#    Via: SIP/2.0/WSS df7jal23ls0d.invalid;branch=z9hG4bK56sdasks
#    From: sip:alice@example.com;tag=asdyka899
#    To: sip:bob@example.com
#    Call-ID: asidkj3ss
#    CSeq: 1 INVITE

#dev
# In request:
# {'content': '',
#  'headers': {'allow': 'INVITE,ACK,CANCEL,BYE,UPDATE',
#              'call-id': 'jbq7mbtn47lqroed9e34im',
#              'contact': [{'name': None,
#                           'params': {'+sip.ice': None,
#                                      '+sip.instance': '"<urn:uuid:fbd0311d-3862-4c3d-9d3b-99e84d837bec>"',
#                                      'expires': '600',
#                                      'reg-id': '1'},
#                           'uri': 'sip:mb786557@js0rrtrfa8ki.invalid;transport=ws'}],
#              'content-length': 0,
#              'cseq': {'method': 'REGISTER', 'seq': 11},
#              'expires': '600',
#              'from': {'name': '"madragonse"',
#                       'params': {'tag': 'jgqodlr9p3'},
#                       'uri': 'sip:6b86b27@127.0.0.1'},
#              'max-forwards': '68',
#              'supported': 'gruu,outbound\r\n',
#              'to': {'name': None,
#                     'params': {'tag': 'testtagtag'},
#                     'uri': 'sip:6b86b27@127.0.0.1'},
#              'via': [{'host': 'js0rrtrfa8ki.invalid',
#                       'params': {'branch': 'z9hG4bK4451615'},
#                       'port': None,
#                       'protocol': 'WS',
#                       'version': '2.0'}]},
#  'method': '',
#  'type': 0,
#  'uri': '',
#  'version': '2.0'}