########################
# SERVER STATE VARIABLES#
########################

# User login sessions
# userid (string) is key, contains dict with 'session_token' and 'refresh_token'
# ex. tkn=Sessions['3']['refresh_token'] gets refresh token for playerId 3
Sessions = {}

################
# COMMON CLASSES#
################

class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
