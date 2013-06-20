import webapp2
from models import Bunny
from google.appengine.api import users
import json
from auth import AuthHandler


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
        # bunnies = JSONEncoder.encode()
        bunnies = json.dumps(bunnies)
        #print bunnies
        #This function was not giving me a correct response at like 2 AM, so I think I fixed it, but I'm not a Python expert so idk if what I did was correct
        self.response.write(bunnies)
        return webapp2.Response(bunnies)


class add_bunny(AuthHandler):
    def post(self):
        # TODO: check to see params exist
        # TODO: get attached bunnies
        lecture_id = self.request.get("lecture_id")
        creator_id = users.get_current_user().user_id()
        document_id = self.request.get("document_id")
        note = self.request.get("note")

        # Send Bunny to Database
        bunny = Bunny(lecture_id=lecture_id,
                      creator_id=creator_id,
                      document_id=document_id,
                      note=note)
        bunny.put()
        #document Document.get_by_id(int(document_id))
        #document.bunny_ids.append(str(bunny.key.id()))
        #document.put()


class update_bunny(AuthHandler):
    def post(self):
        bunny_id = self.request.get("bunny_id")
        note = self.request.get("note")
        bunny = Bunny.get_by_id(int(bunny_id))
        bunny.note = note
        bunny.put()
