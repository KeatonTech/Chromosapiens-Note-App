from google.appengine.ext import ndb


class User(ndb.Model):
    creator_id = ndb.StringProperty(required=True)
    notebook = ndb.StructuredProperty(Notebook, required=True)


class Notebook(ndb.Model):
    owner_id = ndb.StringProperty()
    bunnies = ndb.StructuredProperty(Bunny, repeated=True)


class Bunny(ndb.Model):
    lecture_id = ndb.IntegerProperty(required=True)     #identifier of lecture
    bunny_id = ndb.IntegerProperty(required=True)       #unique bunny id
    creator_id = ndb.StringProperty(required=True)      #identifier for creator
    rating = ndb.IntegerProperty(required=True)         #note rating
    timestamp = ndb.DateTimeProperty(auto_now_add=True) #timestamp for sorting
    attached_bunnies = ndb.StringProperty()
    note = ndb.TextProperty(required=True)

    @classmethod
    def get_lecture_bunnies(cls, lecture_key):
        return cls.query(lecture_id=lecture_key)

    def get_bunny(cls, this_id):
        return cls.query(bunny_id=this_id)

    def get_user_bunnies_for_lecture(cls, lecture_key, user_key):
        return cls.query(cls, lecture_id=lecture_key, creator_id=user_key)