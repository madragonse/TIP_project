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
def get_code_msg(code, error_msg, via, from_, to, call_id, c_seq):
    content = {'method': ' ', 'uri': ' ',
               'headers': {"via": via, 'from': from_, 'to': to, 'call-id': call_id, 'cseq': c_seq}}

    message = SipMessage.from_dict(content)
    message_ob = message
    message = "SIP/2.0 "+str(code)+" "+str(error_msg)+ message.stringify()[11:]
    return message


def get_trying(via, from_, to, call_id, c_seq, contact=None):

    content = {'method':' ', 'uri':' ', 'headers':{"via":via, 'from':from_, 'to':to, 'call-id':call_id, 'cseq':c_seq} }
    if contact is not None: contact.append['headers']['contact'] = contact

    message = SipMessage.from_dict(content)
    message_ob = message
    message = "SIP/2.0 100 Trying"+message.stringify()[11:]
    return message

def get_ok(via, from_, to, call_id, c_seq, contact=None):
    content = {'method':' ', 'uri':' ', 'headers':{"via":via, 'from':from_, 'to':to, 'call-id':call_id, 'cseq':c_seq} }
    if contact is not None: contact.append['headers']['contact'] = contact

    message = SipMessage.from_dict(content)
    message_ob = message
    message = "SIP/2.0 200 OK"+message.stringify()[11:]
    return message

def get_ack(via, from_, to, call_id, c_seq, contact=None, method=' ', uri=' ', header=None):
    content = {'method':method, 'uri':uri, 'headers':{"via":via, 'from':from_, 'to':to, 'call-id':call_id, 'cseq':c_seq} }
    if contact is not None: contact.append['headers']['contact'] = contact

    message = SipMessage.from_dict(content)
    message_ob = message

    if header is not None:
        message = header+message.stringify()[11:]
    else:
        message = message.stringify()
    return message

def get_bye(via, from_, to, call_id, c_seq, contact=None, method=' ', uri=' ', header=None):
    content = {'method':method, 'uri':uri, 'headers':{"via":via, 'from':from_, 'to':to, 'call-id':call_id, 'cseq':c_seq} }
    if contact is not None: contact.append['headers']['contact'] = contact

    message = SipMessage.from_dict(content)
    message_ob = message

    if header is not None:
        message = header+message.stringify()[11:]
    else:
        message = message.stringify()
    return message

