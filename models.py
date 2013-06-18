from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    notebook_id = ndb.StringProperty()


class Notebook(ndb.Model):
    user_id = ndb.StringProperty()
    document_ids = ndb.StringProperty(repeated=True)


class Document(ndb.Model):
    title = ndb.StringProperty(default="untitled")
    lecture_id = ndb.StringProperty()
    notebook_id = ndb.StringProperty()


class Bunny(ndb.Model):
    lecture_id = ndb.StringProperty(required=True)     #identifier of lecture
    document_id = ndb.StringProperty(required=True)
    creator_id = ndb.StringProperty(required=True)      #identifier for creator
    rating = ndb.IntegerProperty(default=0)         #note rating
    timestamp = ndb.DateTimeProperty(auto_now_add=True) #timestamp for sorting
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