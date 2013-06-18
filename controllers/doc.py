import webapp2


class add_document(webapp2.RequestHandler):
    def post(self):
        print "Adding a document: " + self.request.get("message")


class add_bunny(webapp2.RequestHandler):
    def post(self):
        print "Adding a bunny: " + self.request.get("message")