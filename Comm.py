from google.appengine.api import channel

# Basically just abstracts everything to be room-based, instead of Channel based
# Because we're using normal AJAX requests for most things, this is all very simple
class Streamer:
    rooms = {}
    def connectToRoom(self, roomID, userID):
        if not roomID in self.rooms:
            self.rooms[roomID] = {}
        self.rooms[roomID][userID] = Connection(roomID,userID)
        return self.rooms[roomID][userID].secretToken

    def messageRoom(self, roomID, message):
        if not roomID in self.rooms:
            return False
        for conn in self.rooms[roomID]:
            conn.sendMessage(message)
        return True

# Connection Class handles the actual Channel API stuff
class Connection:
    secretToken = ""
    channelID = ""

    def __init__(self, roomID, userID):
        self.channelID = roomID+":"+userID
        self.secretToken = channel.create_channel(self.channelID)

    def sendMessage(self, message):
        channel.send_message(self.channelID,message)