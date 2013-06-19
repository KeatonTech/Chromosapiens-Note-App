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
                      creator_id=creator_id,
                      note=note)
        bunny.put()


class join_lecture(webapp2.RequestHandler):
    def get(self, lecture_id):
        lecture = Lecture.get_by_id(int(lecture_id))
        google_id = users.get_current_user().user_id()
        documents = Document.query(Document.user_id == users.get_current_user().user_id(),
                                  Document.lecture_id == lecture_id)
        document_count = documents.count()

        template_vals = dict()
        template_vals['lecture'] = lecture

        if document_count == 0:
            new_doc = Document(lecture_id=lecture_id, user_id=google_id)
            new_doc.put()
        else:
            document = documents.get()
            template_vals['document'] = document

        vars.render(self, template_vals, 'workspace.html')

    # def post(self, lecture_id):
    #     # TODO: add lecture to user's lectures
    #     # user = User.get_by_id(users.get_current_user().user_id())
    #     # user.lecture_ids.append(lecture_id)
    #     new_document = Document(lecture_id=lecture_id, user_id=users.get_current_user().user_id())
    #     new_document.put()
    #     render(self, {}, 'workspace.html')
