import webapp2
from models import *


class add_document(webapp2.RequestHandler):
    def post(self):
        document = Document(title=self.request.get("title"), lecture_id=self.request.get("lecture_id"), notebook_id=self.request.get("notebook_id"))
        document.put()
        print "Adding a document: " + self.request.get("message")


class add_bunny(webapp2.RequestHandler):
    def post(self):
        # TODO: check to see params exist
        # TODO: get attached bunnies
        bunny = Bunny(lecture_id=self.request.get("lecture_id"), creator_id=self.request.get("creator_id"),
                      note=self.request.get("note"))
        bunny.put()
        print "Adding a bunny: " + self.request.get("message")