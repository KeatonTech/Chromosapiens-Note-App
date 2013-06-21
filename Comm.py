import random
from models import *
from google.appengine.api import channel
import datetime
import json

# Basically just abstracts everything to be room-based, instead of Channel based
# Because we're using normal AJAX requests for most things, this is all very simple


class streamer:
    rooms = {}

    def connect_to_room(self, roomID, userID):
        streamName = channel.create_channel(roomID + "" + userID)
        ns = Stream(lecture_id=roomID,
                    expires=datetime.datetime.now() + datetime.timedelta(seconds=720),
                    streamToken=roomID + "" + userID)
        ns.put()
        print "Added stream " + str(ns.streamToken) + " to room " + roomID
        return streamName

    def message_room(self, roomID, message):
        rstreams = Stream.query(Stream.lecture_id == roomID)
        json_message = json.dumps(message)
        print "BROADCAST: " + json_message
        for stream in rstreams:
            channel.send_message(stream.streamToken, json_message)
            if stream.expires < datetime.datetime.now():
                stream.key.delete()

    def send_user(self, roomID, userObject):
        self.message_room(roomID, {"cmd": "newUser", "payload": userObject.nickname()})


# Connection Class handles the actual Channel API stuff
class connection:
    secretToken = ""
    channelID = ""

    def __init__(self, roomID, userID):
        self.channelID = roomID + "" + userID
        self.secretToken = channel.create_channel(self.channelID)

    def send_message(self, message):
        channel.send_message(self.secretToken, message)
