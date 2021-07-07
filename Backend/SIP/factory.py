from autobahn.asyncio.websocket import WebSocketServerFactory
import pprint

debugMode = True


# abstraction level above protocol, used for holding all clients connected to the server
# also allows sending message to a specific client
# ex. in SIP PROTOCOL use self.factory.send_to_client(id,msg)
class InterUserCommunicationServerFactory(WebSocketServerFactory):

    def __init__(self):
        WebSocketServerFactory.__init__(self)
        # holds all currently registered sockets
        # key is user_id (middle part of URI) value dict with username and socket
        self.clients = {}
        self.SIP_VERSION = "2.0"

    # adds new client to registered clients
    def register(self, client_id, client_name, socketInstance, expire=30):
        self.clients[client_id] = {
            'name': client_name,
            'socket': socketInstance,
            'peer_id': -1,
            'timeout': None
        }

    # deletes client from registered clients
    def unregister(self, socketInstance):
        for client_id, values in self.clients.copy().items():
            if values['socket'] == socketInstance:
                del self.clients[client_id]
                break

    # returns False if no id can be found
    def get_id_from_username(self, username):
        for client_id, values in self.clients.copy().items():
            if values['name'] == username:
                return client_id

        return False

    def get_username_from_id(self, client_id):
        if client_id not in self.clients.copy():
            return False
        return self.clients[client_id]['name']

    # returns client id by socket
    def get_id_from_socket(self, socket):
        for client_id, values in self.clients.copy().items():
            if values['socket'] == socket:
                return client_id

        return False

    def make_peers(self, first, second):
        if first not in self.clients.copy() or second not in self.clients.copy():
            return False

        self.clients[first]['peer_id'] = second
        self.clients[second]['peer_id'] = first
        return True

    def break_peers(self, first, second):
        if debugMode: print("*Breaking peers: "+str(first)+" , "+str(second))
        if first not in self.clients.copy() or second not in self.clients.copy():
            return False

        self.clients[first]['peer_id'] = -1
        self.clients[second]['peer_id'] = -1
        return True

    # returns peered clients id
    def get_peer(self, socket):
        for client_id, values in self.clients.copy().items():
            if values['socket'] == socket:
                peer_id = self.clients[client_id]['peer_id']
                return peer_id

        return False

    def is_connected(self, client_id):
        return client_id in self.clients.copy()

    # sends a msg to given clientId which is the middle part of the URI
    def send_to_client(self, client_id, msg, isBinary=False):
        if client_id in self.clients.copy():
            socket = self.clients[client_id]['socket']
            socket.sendMessage(payload=msg, isBinary=isBinary)
            return

        print("cannot find to client")

    def print_register(self):
        pprint.pprint(self.clients)