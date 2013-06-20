import webapp2
from models import *
from google.appengine.api import users
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
        notebook_id = self.request.get("notebook-id")
        document = Document(title=title, lecture_id=self.request.get("lecture-id"),
                            notebook_id=self.request.get("notebook-id"))
        document.put()
        notebook = Notebook.get_by_id(int(notebook_id))
        notebook.document_ids.append(str(document.key.id()))
        notebook.put()
        self.redirect('/notebooks/'+notebook_id)


class add_bunny(webapp2.RequestHandler):
    def post(self):
        # TODO: check to see params exist
        # TODO: get attached bunnies
        lecture_id = self.request.get("lecture_id")
        creator_id = users.get_current_user().user_id()
        document_id = self.request.get("document_id")
        note = self.request.get("note")
        
        # Send Bunny to Database
        bunny = Bunny(lecture_id=lecture_id,
                      creator_id=creator_id,
                      document_id=document_id,
                      note=note)
        bunny.put()
        #document Document.get_by_id(int(document_id))
        #document.bunny_ids.append(str(bunny.key.id()))
        #document.put()


# class update_bunny(webapp2.RequestHandler):
#     def post(self, note):


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
            document = Document(lecture_id=lecture_id, user_id=google_id)
            document.put()
        else:
            document = documents.get()

        template_vals['document_id'] = document.key.id()
        template_vals['document_name'] = document.title

        vars.render(self, template_vals, 'workspace.html')

    # def post(self, lecture_id):
    #     # TODO: add lecture to user's lectures
    #     # user = User.get_by_id(users.get_current_user().user_id())
    #     # user.lecture_ids.append(lecture_id)
    #     new_document = Document(lecture_id=lecture_id, user_id=users.get_current_user().user_id())
    #     new_document.put()
    #     render(self, {}, 'workspace.html')
