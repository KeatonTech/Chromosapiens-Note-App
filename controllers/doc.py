import webapp2

class add_note(webapp2.RequestHandler):
    def get(self):
        print "Add message controller"

    def post(self):
        print "Adding a note: " + self.request.get("message")