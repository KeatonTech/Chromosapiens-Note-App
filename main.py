from time import sleep

import webapp2
from google.appengine.api import users

from auth import AuthHandler, GoogleLoginLink

from vars import render
from controllers import api, doc
from models import Notebook, Lecture, Document, Bunny


class MainHandler(webapp2.RequestHandler):
    def get(self):
        render(self, {}, 'index.html')


class NotebookHandler(AuthHandler):
    def get(self, notebook_id):
        template_vals = {'name_of_user': users.get_current_user().nickname()}
        notebook = Notebook.get_by_id(int(notebook_id))
        #get all documents for notebook
        titles = list()
        docs = list()
        for doc in notebook.document_ids:
            docs.append(int(doc))
            titles.append(Document.get_by_id(int(doc)).title)
        template_vals['titles'] = titles
        template_vals['nb_id'] = int(notebook_id)
        template_vals['doc_ids'] = docs
        render(self, template_vals, 'mydocs.html')


class DocumentHandler(AuthHandler):
    def get(self, document_id):
        template_vals = {}
        bunnies_result = Bunny.query(Bunny.document_id == str(document_id)).order(Bunny.timestamp).iter()
        bunnies = []
        for bunny in bunnies_result:
            bunnies.append(bunny)
        template_vals['bunnies'] = bunnies
        template_vals['doc_id'] = document_id
        doc = Document.get_by_id(int(document_id))
        template_vals['doc_name'] = doc.title
        template_vals['lecture_id'] = doc.lecture_id
        render(self, template_vals, 'workspace.html')


class DashboardHandler(AuthHandler):
    def get(self):
        template_vals = dict()
        template_vals['name_of_user'] = users.get_current_user().nickname()
        template_vals['notebooks'] = self.get_notebooks(users.get_current_user().user_id())
        render(self, template_vals, 'dashboard.html')

    def get_notebooks(self, user_id):
        sleep(0.10)
        notebooks = {}
        try:
            # notebook_ids = user.notebook_ids
            notebooks = list()
            # for notebook_id in notebook_ids:
            notebook_iter = Notebook.query(Notebook.user_id == user_id).order(Notebook.title).iter()
            for notebook in notebook_iter:
                notebooks.append(notebook)
        except BaseException:
            pass
        return notebooks

        # def get_lectures(self, user):
        #     lectures = dict()
        #     for lecture_id in user.lecture_ids:
        #         lectures


class RoomHandler(AuthHandler):
    def get(self):
        userObject = users.get_current_user()
        if not userObject:
            return self.redirect(users.create_login_url(self.request.uri))
        userID = userObject.user_id()

        roomID = self.request.get('id')
        if not roomID:
            return self.redirect("/")

        vars.stream_manager.message_room(roomID, "{'event':'join','user':'" + userID + "'}")
        token = vars.stream_manager.connect_to_room(roomID, userID)
        vars.render(self, {'token': token}, 'jstest.html')


routes = [
    # Major Pages
    ('/', MainHandler),
    ('/note', RoomHandler),
    ('/dashboard', DashboardHandler),

    # User pages
    ('/documents/(\d+)', DocumentHandler),
    ('/notebooks/(\d+)', NotebookHandler),

    # User actions
    ('/document/add', doc.add_document),
    ('/notebooks/new', doc.add_notebook),
    ('/lectures/join', doc.join_lecture),

    # API Methods (AJAXylicious)
    ('/api/add_bunny', api.add_bunny),
    ('/api/getbunnies', api.get_bunnies),
    ('/api/update_bunny', api.update_bunny),
    ('/api/google_login_link', GoogleLoginLink),
]

app = webapp2.WSGIApplication(routes=routes, debug=True)
