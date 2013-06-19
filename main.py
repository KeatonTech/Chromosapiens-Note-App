import webapp2
from vars import render

# Controllers
import controllers.doc
from models import User, Notebook, Lecture

from google.appengine.api import users


class MainHandler(webapp2.RequestHandler):
    def get(self):
        render(self, {}, 'index.html')


class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        google_user = users.get_current_user()
        template_vals = {'name_of_user': google_user.nickname()}

        if google_user:
            google_id = google_user.user_id()
            user = User.get_user(google_id=google_id)
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

    # def find_lectures(self, user_id):
        # lecture_iter = Lecture.query(Lecture.start_time )


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
    ('/', MainHandler),
    ('/note', RoomHandler),
    ('/api/append', controllers.doc.add_bunny),
    ('/document/add', controllers.doc.add_document),
    ('/dashboard', DashboardHandler),
                                  ('/notebooks/new', controllers.doc.add_notebook),
], debug=True)
