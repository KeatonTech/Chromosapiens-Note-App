import webapp2
from vars import render
from time import time, sleep

# Controllers
import controllers.doc
from models import User, Notebook, Lecture
import datetime

from google.appengine.api import users


class MainHandler(webapp2.RequestHandler):
    def get(self):
        render(self, {}, 'index.html')


class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        google_user = users.get_current_user()

        if google_user:
            google_id = google_user.user_id()
            user = User.get_user(google_id=google_id)
            template_vals = {'name_of_user': google_user.nickname()}
            if user:
                # print user
                template_vals['notebooks'] = self.get_notebooks(google_id)
                template_vals['lectures'] = self.find_lectures()
                template_vals['message'] = 'Welcome back, ' + user.name + '!'
            else:
                new_user = User(id=google_id, name=google_user.nickname(), email=google_user.email(), notebook_ids=[])
                new_user.put()
                template_vals['message'] = 'Welcome to NoteBunnies! We have finished setting up your account.'
            render(self, template_vals, 'dashboard.html')
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def get_notebooks(self, user_id):
        sleep(0.5)
        notebooks = {}
        try:
            # notebook_ids = user.notebook_ids
            notebooks = list()
            # for notebook_id in notebook_ids:
            notebook_iter = Notebook.query(Notebook.user_id == user_id).iter()
            for notebook in notebook_iter:
                notebooks.append(notebook)
        except BaseException:
            pass
        return notebooks

    def find_lectures(self):
        # time_window = datetime.datetime.now() - datetime.timedelta(days=3)
        lectures = Lecture.query().order(Lecture.created_at).fetch(limit=10)
        return lectures


class RoomHandler(webapp2.RequestHandler):
    def get(self):
        userObject = users.get_current_user()
        if not userObject:
            return self.redirect(users.create_login_url(self.request.uri))
        userID = userObject.user_id()

        roomID = self.request.get('id')
        if not roomID:
            return self.redirect("/")

        vars.stream_manager.message_room(roomID, "{'event':'join','user':'" + userID + "'}")
        token = vars.stream_manager.connect_to_room(roomID, userID)
        vars.render(self, {'token': token}, 'jstest.html')


app = webapp2.WSGIApplication([
                                  # Major Pages
                                  ('/', MainHandler),
                                  ('/note', RoomHandler),

                                  # API Methods (AJAXylicious)
                                  ('/api/append', controllers.doc.add_bunny),
                                  ('/document/add', controllers.doc.add_document),
                                  ('/dashboard', DashboardHandler),
                                  ('/notebooks/new', controllers.doc.add_notebook),
                                  ('/lectures/add', controllers.doc.add_lecture),
                              ], debug=True)
