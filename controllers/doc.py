from auth import AuthHandler
from models import *
from google.appengine.api import users
import vars


class add_notebook(AuthHandler):
    def post(self):
        title = self.request.get("notebook-title")
        google_id = users.get_current_user().user_id()
        new_notebook = Notebook(user_id=google_id, title=title, document_ids=[])
        new_notebook.put()
        self.redirect('/dashboard')


class add_document(AuthHandler):
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


class join_lecture(AuthHandler):
    def post(self):
        lecture_id = self.request.get("lecture_id")
        lecture = Lecture.get_by_id(lecture_id)
        if lecture:
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

            user = User.get_user(google_id)
            if lecture_id not in user.lecture_ids:
                user.lecture_ids.append(lecture_id)
                user.put()

            template_vals['document_id'] = document.key.id()
            template_vals['document_name'] = document.title

            vars.render(self, template_vals, 'workspace.html')
        else:
            # Do with ajax instead; won't keep old notebooks
            vars.render(self, {'message': 'Lecture is invalid.'}, 'dashboard.html')


class new_lecture(AuthHandler):
    def post(self):
        lecture_name = str(self.request.get("lecture_id"))
        new_lecture = Lecture(id=lecture_name, name=lecture_name, creator=users.get_current_user().user_id())
        new_lecture.put()
        
        google_id = users.get_current_user().user_id()
        user = User.get_user(google_id)
        user.lecture_ids.append(lecture_name)
        user.put()
        
        template_vals = dict()
        template_vals['lecture_id'] = lecture_name

        vars.render(self, template_vals, 'managelecture.html')

    # def post(self, lecture_id):
    #     # TODO: add lecture to user's lectures
    #     # user = User.get_by_id(users.get_current_user().user_id())
    #     # user.lecture_ids.append(lecture_id)
    #     new_document = Document(lecture_id=lecture_id, user_id=users.get_current_user().user_id())
    #     new_document.put()
    #     render(self, {}, 'workspace.html')
