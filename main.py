import webapp2
import vars

# Controllers
import controllers.doc

from google.appengine.api import users


class MainHandler(webapp2.RequestHandler):
    def get(self):
        vars.render(self, {}, 'index.html')


class RoomHandler(webapp2.RequestHandler):
    def get(self):
        userObject = users.get_current_user()
        if not userObject:
            return self.redirect(users.create_login_url(self.request.uri))
        userID = userObject.user_id()

        roomID = self.request.get('id')
        if not roomID:
            return self.redirect("/")

        vars.streamManager.message_room(roomID, "{'event':'join','user':'"+userID+"'}")
        token = vars.streamManager.connect_to_room(roomID,userID)
        vars.render(self, {'token': token}, 'jstest.html')


app = webapp2.WSGIApplication([
    # Major Pages
    ('/', MainHandler),
    ('/note', RoomHandler),
    
    # API Methods (AJAXylicious)
    ('/api/append', controllers.doc.add_bunny),
    ('/document/add', controllers.doc.add_document),
], debug=True)
