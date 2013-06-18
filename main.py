import webapp2
import jinja2
import os


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates/"),
    extensions=['jinja2.ext.autoescape'])


def render(self, template_values, template_url):
    template = JINJA_ENVIRONMENT.get_template(template_url)
    self.response.write(template.render(template_values))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        render(self, {}, 'index.html')


class RegistrationHandler(webapp2.RequestHandler):
    def get(self):
        render(self, {}, 'register.html')


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        render(self, {}, 'login.html')


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        render(self, {}, 'logout.html')


class AccountPage(webapp2.RequestHandler):
    def get(self):
        render(self, {}, 'account.html')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegistrationHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/account', AccountPage),
], debug=True)
