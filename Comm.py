import random
from models import *
from google.appengine.api import channel

# Basically just abstracts everything to be room-based, instead of Channel based
# Because we're using normal AJAX requests for most things, this is all very simple
class streamer:
    rooms = {}
    def connect_to_room(self, roomID, userID):
        if not roomID in self.rooms:
            self.rooms[roomID] = {}
        self.rooms[roomID][userID] = connection(roomID,userID)
        return self.rooms[roomID][userID].secretToken
	
    def message_room(self, roomID, message):
        if not roomID in self.rooms:
            return False
        for userKey in self.rooms[roomID]:
            self.rooms[roomID][userKey].send_message(message)
        return True
	
	def send-user(self, roomID, userObject):
		self.message_room(roomID,{cmd: "newUser", payload: userObject});
		
	def logout-user(self, roomID, userID):
		self.message_room(roomID,{cmd: "deleteUser", id: userID});
	
	def send-bunny(self, roomID, bunnyObject):
		self.message_room(roomID,{cmd: "newBunny", payload: bunnyObject});
	
	def send-bunny-update(self, roomID, bunnyObject):
		self.message_room(roomID,{cmd: "bunnyUpdate", id: bunnyObject.id, payload: bunnyObject});
	
	def bunny-death-ray(self, roomID, bunnyID):
		self.message_room(roomID,{cmd: "deleteBunny", id: bunnyID});

# Connection Class handles the actual Channel API stuff
class connection:
    secretToken = ""
    channelID = ""

    def __init__(self, roomID, userID):
        # Channel ID includes a random component for some added security, just in case
        self.channelID = roomID+":"+userID+":"+str(random.randint(100000,999999))
        self.secretToken = channel.create_channel(self.channelID)

    def send_message(self, message):
        channel.send_message(self.channelID,message)
