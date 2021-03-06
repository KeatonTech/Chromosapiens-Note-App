from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    notebook_ids = ndb.StringProperty(repeated=True)
    lecture_ids = ndb.StringProperty(repeated=True)
    tutorial = ndb.StringProperty(default="yes")
    
    @classmethod
    def get_user(cls, google_id):
        return User.get_by_id(google_id)


class Stream(ndb.Model):
    lecture_id = ndb.StringProperty()
    streamToken = ndb.StringProperty()
    streamSecret = ndb.StringProperty()
    expires = ndb.DateTimeProperty()

    
class Notebook(ndb.Model):
    user_id = ndb.StringProperty()
    title = ndb.StringProperty()
    lecture_id = ndb.StringProperty()
    document_ids = ndb.StringProperty(repeated=True)
    created_at = ndb.DateProperty(auto_now_add=True)
    color = ndb.StringProperty(default="6")


class Document(ndb.Model):
    title = ndb.StringProperty(default="untitled document")
    lecture_id = ndb.StringProperty()
    notebook_id = ndb.StringProperty()
    user_id = ndb.StringProperty()


class Lecture(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    creator = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    is_active = ndb.BooleanProperty(default=False)


class Bunny(ndb.Model):
    lecture_id = ndb.StringProperty(required=True)
    document_id = ndb.StringProperty(required=True)
    creator_id = ndb.StringProperty(required=True)
    title = ndb.StringProperty()
    rating = ndb.IntegerProperty(default=0)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    attached_bunnies = ndb.StringProperty(repeated=True)
    note = ndb.TextProperty(required=True)

    @classmethod
    def get_lecture_bunnies(cls, lecture_key):
        return cls.query(lecture_id=lecture_key)

    @classmethod
    def get_bunny(cls, this_id):
        return cls.query(bunny_id=this_id)

    @classmethod
    def get_user_bunnies_for_lecture(cls, lecture_key, user_key):
        return cls.query(cls, lecture_id=lecture_key, creator_id=user_key)