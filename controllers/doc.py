import webapp2
from models import *
from google.appengine.api import users
from vars import render
import vars


class add_lecture(webapp2.RequestHandler):
    def post(self):
        lecture_id = self.request.get("lecture-id")
        print lecture_id
        self.redirect('/dashboard')


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
        self.redirect('/dashboard')


class add_bunny(webapp2.RequestHandler):
    def post(self):
        # TODO: check to see params exist
        # TODO: get attached bunnies
        
        # Send Bunny to Database
        bunny = Bunny(lecture_id=self.request.get("lecture_id"),
                      creator_id=self.request.get("creator_id"),
                      note=self.request.get("note"))
        bunny.put()

        print "Adding a bunny: " + self.request.get("message")