from sip_parser.exceptions import SipParseError
from sip_parser.sip_message import SipMessage
import pprint.pprint as pprint


def get_trying():
    message = SipMessage.from_dict({"method":})
    pprint(message.stringify())




#    SIP/2.0 100 Trying
#    Via: SIP/2.0/WSS df7jal23ls0d.invalid;branch=z9hG4bK56sdasks
#    From: sip:alice@example.com;tag=asdyka899
#    To: sip:bob@example.com
#    Call-ID: asidkj3ss
#    CSeq: 1 INVITE