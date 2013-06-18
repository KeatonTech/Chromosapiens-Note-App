import webapp2
import jinja2
import os
import comm

from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates/"),
    extensions=['jinja2.ext.autoescape'])


def render(self, template_values, template_url):
    template = JINJA_ENVIRONMENT.get_template(template_url)
    self.response.write(template.render(template_values))

streamManager = comm.streamer()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        render(self, {}, 'index.html')

class RoomHandler(webapp2.RequestHandler):
    def get(self):
        userObject = users.get_current_user()
        if not userObject:
            return self.redirect(users.create_login_url(self.request.uri))
        userID = userObject.user_id()

        roomID = self.request.get('id')
        if not roomID:
            return self.redirect("/")

        streamManager.message_room(roomID, "{'event':'join','user':'"+userID+"'}")
        token = streamManager.connect_to_room(roomID,userID)
        render(self, {'token': token}, 'jstest.html')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/room', RoomHandler),
], debug=True)
