from sip_parser.exceptions import SipParseError
from sip_parser.sip_message import SipMessage


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

def get_bye(via, from_, to, call_id, c_seq, contact=None, method=' ', uri=' ', header=None):
    content = {'method':method, 'uri':uri, 'headers':{"via":via, 'from':from_, 'to':to, 'call-id':call_id, 'cseq':c_seq} }
    if contact is not None: contact.append['headers']['contact'] = contact

    message = SipMessage.from_dict(content)
    message_ob = message

    if header is not None:
        message = header+message.stringify()[11:]
    else:
        message = message.stringify()
    return message, message_ob

