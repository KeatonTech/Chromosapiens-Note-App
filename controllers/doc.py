import webapp2
import vars

class add_document(webapp2.RequestHandler):
    def post(self):
        print "Adding a document: " + self.request.get("message")


class add_bunny(webapp2.RequestHandler):
    def post(self):
        room = self.request.get("room_id")
        if not room: return 
        user = self.request.get("user_id")
        print "Adding a bunny: " + self.request.get("message")