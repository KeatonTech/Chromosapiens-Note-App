from models import Bunny, Stream
from google.appengine.api import users
import json
import vars
from auth import AuthHandler
import webapp2


class get_bunnies(AuthHandler):
    def get(self):
        document_id = self.request.get("document_id")
        bunnies_result = Bunny.query(Bunny.document_id == str(document_id)).order(Bunny.timestamp).iter()
        bunnies = dict()
        for bunny in bunnies_result:
            print bunny.note
            raw_bunny = bunny
            bunny = bunny.to_dict()
            bunny['timestamp'] = str(bunny['timestamp'])
            bunnies[raw_bunny.key.id()] = bunny
        bunnies = json.dumps(bunnies)
        self.response.write(bunnies)


class add_bunny(AuthHandler):
    def post(self):
        # TODO: check to see params exist
        # TODO: get attached bunnies
        lecture_id = self.request.get("lecture_id")
        creator_id = users.get_current_user().user_id()
        document_id = self.request.get("document_id")
        title = self.request.get("title")
        note = self.request.get("note")

        # Send Bunny to Database
        bunny = Bunny(lecture_id=lecture_id,
                      creator_id=creator_id,
                      document_id=[document_id],
                      note=note,
                      title=title)
        bunny.put()
        self.response.write(bunny.key.id());
        safe_bunny = bunny.to_dict()
        safe_bunny['timestamp'] = str(safe_bunny['timestamp'])
        vars.stream_manager.message_room(lecture_id,{'cmd': "newBunny", 'payload': safe_bunny});
        #document Document.get_by_id(int(document_id))
        #document.bunny_ids.append(str(bunny.key.id()))
        #document.put()


class update_bunny(AuthHandler):
    def post(self):
        bunny_id = self.request.get("bunny_id")
        note = self.request.get("note")
        title = self.request.get("title")
        bunny = Bunny.get_by_id(int(bunny_id))
        bunny.note = note
        bunny.title = title
        bunny.put()
        
        safe_bunny = bunny.to_dict()
        safe_bunny['timestamp'] = str(safe_bunny['timestamp'])
        vars.stream_manager.message_room(bunny.lecture_id,{'cmd': "updateBunny", 'payload': safe_bunny});

class delete_bunny(AuthHandler):
    def post(self):
        bunny_id = self.request.get("bunny_id")
        bunny = Bunny.query(Bunny.id == bunny_id)
        bunny.delete()

class link_bunny(AuthHandler):
    def post(self):
        bunny_id = self.request.get("bunny_id")
        bunny = Bunny.query(Bunny.id == bunny_id)
        
        
class disconnect(webapp2.RequestHandler):
    def post(self):
        stream_token = self.request.get("stream_token")
        stream = Stream.query(Stream.streamSecret == stream_token).get()
        stream.key.delete()
        self.response.write("Disconnected")
        vars.stream_manager.message_room(stream.lecture_id,{'cmd': "removeUser", 'id': users.get_current_user().user_id()});