import webapp2
from models import Bunny
import json


class get_bunnies(webapp2.RequestHandler):
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
        for bunny in bunnies:
            print str(bunny['note'])
        bunnies = json.dumps(bunnies)

        return webapp2.Response(bunnies)