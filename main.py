from time import sleep

import webapp2
from google.appengine.api import users

from vars import render
from controllers import api, doc
from models import User, Notebook, Lecture, Document, Bunny


class AuthHandler(webapp2.RequestHandler):
    def dispatch(self):
        google_user = users.get_current_user()
        if google_user:
            google_id = google_user.user_id()
            user = User.get_user(google_id=google_id)
            if user:
                super(AuthHandler, self).dispatch()
            else:
                new_user = User(id=google_id, name=google_user.nickname(), email=google_user.email(), notebook_ids=[])
                new_user.put()
                template_vals = {'name_of_user': google_user.nickname()}
                template_vals['message'] = 'Welcome to NoteBunnies! We have finished setting up your account.'
                render(self, template_vals, 'dashboard.html')
        else:
            self.redirect(users.create_login_url(self.request.uri))


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
        template_vals={}
        bunnies_result = Bunny.query(Bunny.document_id == str(document_id)).order(Bunny.timestamp).iter()
        bunnies = []
        for bunny in bunnies_result:
            bunnies.append(bunny)
        template_vals['bunnies'] = bunnies
        template_vals['doc_id'] = document_id
        doc = Document.get_by_id(int(document_id))
        template_vals['doc_name'] = doc.title
        template_vals['lecture'] = doc.lecture_id
        render(self, template_vals, 'workspace.html')


class DashboardHandler(AuthHandler):
    def get(self):
        template_vals = dict()
        template_vals['name_of_user'] = users.get_current_user().nickname()
        template_vals['notebooks'] = self.get_notebooks(users.get_current_user().user_id())
        template_vals['lectures'] = self.find_lectures()
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

    def find_lectures(self):
        # time_window = datetime.datetime.now() - datetime.timedelta(days=3)
        lectures = Lecture.query().order(Lecture.created_at).fetch(limit=10)
        return lectures

    # def get_lectures(self, user):
    #     lectures = dict()
    #     for lecture_id in user.lecture_ids:
    #         lectures


class RoomHandler(webapp2.RequestHandler):
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


app = webapp2.WSGIApplication([
                                  # Major Pages
                                  ('/', MainHandler),
                                  ('/note', RoomHandler),

                                  # API Methods (AJAXylicious)
                                  ('/document/add', doc.add_document),
                                  ('/api/add_bunny', doc.add_bunny),
                                  ('/dashboard', DashboardHandler),
                                  ('/notebooks/new', doc.add_notebook),
                                  ('/notebooks/(\d+)', NotebookHandler),
                                  ('/documents/(\d+)', DocumentHandler),
                                  # ('/lectures/add', controllers.doc.add_lecture),
                                  ('/lectures/(\d+)', doc.join_lecture),
                                  ('/api/getbunnies', api.get_bunnies),
                              ], debug=True)
