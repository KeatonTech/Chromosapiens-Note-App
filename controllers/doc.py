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
        self.redirect('/dashboard')
        # vars.render(self, {'message': 'Created notebook '+title+'.'}, 'dashboard.html')


class add_document(webapp2.RequestHandler):
    def post(self):
        title = self.request.get("document-title")
        document = Document(title=title, lecture_id=self.request.get("lecture-id"),
                            notebook_id=self.request.get("notebook-id"))
        document.put()
        print "Adding a document: " + self.request.get("message")
        self.redirect('/dashboard')


class add_bunny(webapp2.RequestHandler):
    def post(self):
        # TODO: check to see params exist
        # TODO: get attached bunnies
        lecture_id = self.request.get("lecture_id")
        creator_id = users.get_current_user().user_id()
        note = self.request.get("note")

        # Send Bunny to Database
        bunny = Bunny(lecture_id=lecture_id,
                      creator_id=self.request.get("creator_id"),
                      note=self.request.get("note"))
        bunny.put()

        print "Adding a bunny: " + self.request.get("message")


class join_lecture(webapp2.RequestHandler):
    def get(self, lecture_id):
        lecture = Lecture.get_by_id(int(lecture_id))
        # TODO: prepare document when user joins lecture. Should not be in database till user starts typing. On revisit,
        # check to see if document already exists. Consider separating GET/POST
        document = Document.query(Document.user_id == users.get_current_user().user_id(),
                                  Document.lecture_id == lecture_id)
        for doc in document:
            print doc
        # TODO: CSS can't be found in /lectures/ subdirectory
        vars.render(self, {'lecture': lecture}, 'workspace.html')

    # def post(self, lecture_id):
    #     # TODO: add lecture to user's lectures
    #     # user = User.get_by_id(users.get_current_user().user_id())
    #     # user.lecture_ids.append(lecture_id)
    #     new_document = Document(lecture_id=lecture_id, user_id=users.get_current_user().user_id())
    #     new_document.put()
    #     render(self, {}, 'workspace.html')
