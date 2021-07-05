from SIP.messages import get_trying, get_ok, get_ack
from pprint import pprint as pretty


ret = get_ack(header="ACK sip:bob@203.0.113.22:5060 SIP/2.0", via=[{'host': 'df7jal23ls0d.invalid','params': {'branch': 'z9hG4bK56sdasks'},'port': None,'protocol': 'WS', 'version': '2.0'}],\
    from_="sip:alice@example.com;tag=asdyka899", to="sip:bob@example.com", call_id="asidkj3ss", c_seq="1 ACK")

print(ret[0])

