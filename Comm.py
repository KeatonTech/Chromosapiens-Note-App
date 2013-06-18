from google.appengine.api import channel
from google.appengine.api import users

# Basically just abstracts everything to be room-based, instead of Channel based
# Because we're using normal AJAX requests for most things, this is all very simple
class Streamer:
	rooms = {}
	def connectToRoom(self, roomID):
		if not roomID in rooms:
			rooms[roomID] = {}
		userID = users.get_current_user()
		rooms[roomID][userID] = Connection(roomID,userID)
		return rooms[roomID][userID].secretToken
	
	def messageRoom(self, roomID, message):
		if not roomID in rooms:
			return False
		for conn in rooms[roomID]:
			conn.sendMessage(message)
		return True
		
# Connection Class handles the actual Channel API stuff
class Connection:
	secretToken = ""
	channelID = ""
	
	def __init__(self, roomID, userID):
		channelID = roomID+":"+userID
		secretToken = channel.createChannel()
		
	def sendMessage(self, message):
		channel.sendMessage(channelID,message)