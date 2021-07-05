from SIP.messages import get_trying, get_ok, get_ack
from pprint import pprint as pretty



# ret = get_trying(via=[{'host': 'df7jal23ls0d.invalid','params': {'branch': 'z9hG4bK56sdasks'},'port': None,'protocol': 'WS', 'version': '2.0'}],\
#     from_="sip:alice@example.com;tag=asdyka899", to="sip:bob@example.com", call_id="asidkj3ss", c_seq="1 INVITE")
# print(ret[0])

ret = get_ack(header="ACK sip:bob@203.0.113.22:5060 SIP/2.0", via=[{'host': 'df7jal23ls0d.invalid','params': {'branch': 'z9hG4bK56sdasks'},'port': None,'protocol': 'WS', 'version': '2.0'}],\
    from_="sip:alice@example.com;tag=asdyka899", to="sip:bob@example.com", call_id="asidkj3ss", c_seq="1 ACK")

print(ret[0])



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

# ACK sip:bob@203.0.113.22:5060 SIP/2.0
# Via: SIP/2.0/WS df7jal23ls0d.invalid;branch=z9hG4bK56sdasks
# From: sip:alice@example.com;tag=asdyka899
# To: sip:bob@example.com
# Call-ID: asidkj3ss
# Cseq: 1 ACK
# Content-Length: 0

# ACK sip:bob@203.0.113.22:5060 SIP/2.0
# Via: SIP/2.0/WS df7jal23ls0d.invalid;branch=z9hG4bK56sdasks
# From: sip:alice@example.com;tag=asdyka899
# To: sip:bob@example.com
# Call-ID: asidkj3ss
# Cseq: 1 ACK
# Content-Length: 0

#dev
# SIP/2.0 100 Trying
# Via: SIP/2.0/WS df7jal23ls0d.invalid;branch=z9hG4bK56sdasks
# From: sip:alice@example.com;tag=asdyka899
# To: sip:bob@example.com
# Call-ID: asidkj3ss
# CSeq: 1 INVITE

#dev
# SIP/2.0 100 Trying
# Via: SIP/2.0/WS df7jal23ls0d.invalid;branch=z9hG4bK56sdasks
# From: sip:alice@example.com;tag=asdyka899
# To: sip:bob@example.com
# Call-ID: asidkj3ss
# Cseq: 1 INVITE
# Content-Length: 0