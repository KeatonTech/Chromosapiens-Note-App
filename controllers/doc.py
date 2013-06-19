import webapp2
from models import *
from google.appengine.api import users
from vars import render
import vars


class add_notebook(webapp2.RequestHandler):
    def post(self):
        title = self.request.get("notebook-title")
        google_id = users.get_current_user().user_id()
        new_notebook = Notebook(user_id=google_id, title=title, document_ids=[])
        new_notebook.put()
        # if Notebook.get_by_id(new_notebook.key.id()):
        # TODO: Reload page so user will see new notebook
        self.redirect('/dashboard')
        # vars.render(self, {'message': 'Created notebook '+title+'.'}, 'dashboard.html')


class add_document(webapp2.RequestHandler):
    def post(self):
        title = self.request.get("document-title")
        document = Document(title=title, lecture_id=self.request.get("lecture_id"),
                            notebook_id=self.request.get("notebook_id"))
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


class register(webapp2.RequestHandler):
    def post(self):
        if users.get_current_user():
            name = self.request.get("name")
            email = self.request.get("email")
            user_id = users.get_current_user().user_id()
            new_notebook = Notebook(user_id=user_id, document_ids=[])
            new_notebook.put()
            notebook_ids = list()
            notebook_ids.append(new_notebook.key)
            new_user = User(user_id=user_id, name=name, email=email, notebook_ids=notebook_ids)
            new_user.put()

    def get(self):
        render(self, {}, 'register.html')