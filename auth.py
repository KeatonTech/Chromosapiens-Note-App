import webapp2
from google.appengine.api import users
from models import User
from vars import render


class AuthHandler(webapp2.RequestHandler):
    def dispatch(self):
        google_user = users.get_current_user()
        if google_user:
            google_id = google_user.user_id()
            user = User.get_user(google_id=google_id)
            if user:
                super(AuthHandler, self).dispatch()
            else:
                new_user = User(id=google_id, name=google_user.nickname(), email=google_user.email(), notebook_ids=[])
                new_user.put()
                template_vals = {'name_of_user': google_user.nickname()}
                template_vals['message'] = 'Welcome to NoteBunnies! We have finished setting up your account.'
                render(self, template_vals, 'dashboard.html')
        else:
            self.redirect('/')


class GoogleLoginLink(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_login_url(self.request.uri))