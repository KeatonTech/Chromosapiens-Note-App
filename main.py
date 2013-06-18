import webapp2
import jinja2
import os
import Comm.py

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates/"),
    extensions=['jinja2.ext.autoescape'])

def render(self, template_values, template_url):
    template = JINJA_ENVIRONMENT.get_template(template_url)
    self.response.write(template.render(template_values))

streamManager = Streamer()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        render(self, {}, 'index.html')


class RoomHandler(webapp2.RequestHandler):
    def get(self):

        userID = users.get_current_user()
        if not user:
            return self.redirect(users.create_login_url(self.request.uri))

        roomID = self.request.get('room')
        if not room:
            return self.redirect("/")

        token = streamManager.connectToRoom(roomID,userID)
        self.response.write(token)


app = webapp2.WSGIApplication([
    ('/', MainHandler),

], debug=True)
