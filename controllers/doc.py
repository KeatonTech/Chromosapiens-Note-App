from auth import AuthHandler
from models import *
from google.appengine.api import users
import vars
import json


class add_notebook(AuthHandler):
    def post(self):
        title = self.request.get("notebook-title")
        google_id = users.get_current_user().user_id()
        new_notebook = Notebook(user_id=google_id, title=title, document_ids=[])
        new_notebook.put()
        self.redirect('/dashboard')


class delete_notebook(AuthHandler):
    def get(self):
        nb_id = self.request.get("notebook-id")
        notebook = Notebook.get_by_id(int(nb_id))
        google_id = users.get_current_user().user_id()
        user = User.get_user(google_id)
        user.lecture_ids.remove(notebook.lecture_id)
        user.put()
        notebook.key.delete()
        
        self.redirect('/dashboard')


class add_document(AuthHandler):
    def post(self):
        title = self.request.get("document-title")
        notebook_id = self.request.get("notebook-id")
        print notebook_id
        document = Document(title=title, lecture_id=self.request.get("lecture-id"),
                            notebook_id=self.request.get("notebook-id"), user_id=users.get_current_user().user_id())
        document.put()
        notebook = Notebook.get_by_id(int(notebook_id))
        notebook.document_ids.append(str(document.key.id()))
        notebook.put()
        self.redirect('/notebooks/' + notebook_id)


class change_notebook_color(AuthHandler):
    def get(self):
        nb = Notebook.get_by_id(int(self.request.get("notebook_id")))
        nb.color = self.request.get("color")
        nb.put()
        self.redirect('/dashboard')


class join_lecture(AuthHandler):
    def get(self):
        print "We're here"
        lecture_id = self.request.get("lecture_id")
        # lecture_future = Lecture.get_by_id_async(lecture_id)
        notebook = Notebook.query(Notebook.lecture_id == lecture_id).get()
        documents = Document.query(Document.lecture_id == lecture_id,
                                   Document.user_id == users.get_current_user().user_id())

        template_vals = dict()
        # template_vals['lecture'] = lecture_future.get_result()
        template_vals['notebook_id'] = notebook.key.id()
        template_vals['lecture_id'] = lecture_id
        template_vals['documents'] = documents
        template_vals['document_id'] = documents.get().key.id()
		
		# Token for the streaming API
        vars.stream_manager.send_user(lecture_id,users.get_current_user())
        template_vals['streamToken'] = vars.stream_manager.connect_to_room(lecture_id,users.get_current_user().user_id())
		
        vars.render(self, template_vals, 'workspace.html')

    def post(self):
        lecture_id = self.request.get("lecture_id")
        lecture = Lecture.get_by_id(lecture_id)
        template_vals = {'message': "Lecture invalid."}
        if lecture:
            google_id = users.get_current_user().user_id()

            notebooks = Notebook.query(Notebook.lecture_id == lecture_id)

            if notebooks.count == 0:

                notebook = Notebook(title=lecture_id + ' Notes', lecture_id=lecture_id, user_id=google_id)
                future_notebook = notebook.put_async()

                document = Document(lecture_id=lecture_id, notebook_id=str(future_notebook.get_result().id()),
                                    user_id=google_id)
                future_document = document.put_async()

                user = User.get_user(google_id)
                # if lecture_id not in user.lecture_ids:
                user.lecture_ids.append(lecture_id)
                user.put()

                template_vals['lecture_id'] = lecture.key.id()
                template_vals['document_id'] = future_document.get_result().id()
                template_vals['notebook_name'] = lecture_id + 'Notes'

                # self.response.write(json.dumps(template_vals))

            else:
                template_vals['message'] = "Lecture already added."

        vars.render(self, template_vals, 'workspace.html')
        # self.response.write(template_vals)


class new_lecture(AuthHandler):
    def post(self):
        lecture_id = str(self.request.get("lecture_id"))
        google_id = users.get_current_user().user_id()

        lecture = Lecture.get_by_id(lecture_id)

        if lecture:
            vars.render(self, {'message': 'This name already exists.'}, 'dashboard.html')
        else:
            new_lecture = Lecture(id=lecture_id, name=lecture_id, creator=google_id)
            future_new_lecture = new_lecture.put_async()

            notebook = Notebook(title=lecture_id + ' Notes', lecture_id=lecture_id, user_id=google_id)
            future_notebook = notebook.put_async()

            document = Document(lecture_id=lecture_id, notebook_id=str(future_notebook.get_result().id()),
                                user_id=google_id)
            future_document = document.put_async()

            user = User.get_user(google_id)
            user.lecture_ids.append(lecture_id)
            user.put()

            future_document.get_result()
            future_new_lecture.get_result()

            self.redirect('/dashboard')
