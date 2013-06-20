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


class delete_notebook(AuthHandler):
    def post(self):
        nb_id = self.request.get("notebook-id")
        notebook = Notebook.get_by_id(int(nb_id))
        notebook.key.delete()

        self.redirect('/dashboard')


class add_document(AuthHandler):
    def post(self):
        title = self.request.get("document-title")
        notebook_id = self.request.get("notebook-id")
        document = Document(title=title, lecture_id=self.request.get("lecture-id"),
                            notebook_id=self.request.get("notebook-id"), user_id=users.get_current_user().user_id())
        document.put()
        notebook = Notebook.get_by_id(int(notebook_id))
        notebook.document_ids.append(str(document.key.id()))
        notebook.put()
        self.redirect('/notebooks/' + notebook_id)

class change_notebook_color(AuthHandler):
    def post(self):
        Notebook.set_color(self.request.get("notebook_id"), self.request.get("color"))
        self.redirect('/dashboard')
        
class join_lecture(AuthHandler):
    def get(self):
        lecture_id = self.request.get("lecture_id")
        # lecture_future = Lecture.get_by_id_async(lecture_id)
        document = Document.query(Document.lecture_id == lecture_id).get()
        
        template_vals = dict()
        # template_vals['lecture'] = lecture_future.get_result()
        template_vals['lecture_id'] = lecture_id
        template_vals['document_id'] = document.key.id()
        template_vals['document_name'] = document.title
        template_vals['notebook_name'] = Notebook.get_by_id(int(document.notebook_id)).title
        vars.render(self, template_vals, 'workspace.html')

    def post(self):
        lecture_id = self.request.get("lecture_id")
        notebook_id = self.request.get("notebook_id")
        lecture = Lecture.get_by_id(lecture_id)
        if lecture:
            google_id = users.get_current_user().user_id()
            documents = Document.query(Document.user_id == google_id,
                                       Document.lecture_id == lecture_id)
            document_count = documents.count()

            template_vals = dict()
            template_vals['lecture'] = lecture

            if document_count == 0:
                document = Document(lecture_id=lecture_id, user_id=google_id, notebook_id=notebook_id)
                document.put()
            else:
                document = documents.get()

            user = User.get_user(google_id)
            if lecture_id not in user.lecture_ids:
                user.lecture_ids.append(lecture_id)
                user.put()

            template_vals['document_id'] = document.key.id()
            template_vals['document_name'] = document.title
            template_vals['notebook_name'] = Notebook.get_by_id(int(notebook_id)).title

            vars.render(self, template_vals, 'workspace.html')
        else:
            # Bug: Do with ajax instead; won't keep old notebooks
            vars.render(self, {'message': 'Lecture is invalid.'}, 'dashboard.html')


class new_lecture(AuthHandler):
    def post(self):
        lecture_name = str(self.request.get("lecture_id"))
        notebook_id = str(self.request.get("notebook_id"))
        new_lecture = Lecture(id=lecture_name, name=lecture_name, creator=users.get_current_user().user_id())
        new_lecture.put()

        google_id = users.get_current_user().user_id()
        user = User.get_user(google_id)
        user.lecture_ids.append(lecture_name)
        user.put()

        # TODO: add notebook id (popup window)
        document = Document(lecture_id=lecture_name, user_id=google_id, notebook_id=notebook_id)
        document.put()

        template_vals = dict()
        template_vals['lecture_id'] = lecture_name

        self.redirect('/dashboard')
