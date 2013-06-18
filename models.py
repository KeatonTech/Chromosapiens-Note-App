from google.appengine.ext import ndb

class User(ndb.Model):
    creatorid = ndb.StringProperty(required=True)
    notebook = ndb.StructuredProperty(Notebook, required=True)
	
class Notebook(ndb.Model):
    ownerid = ndb.StringProperty()
    bunnies = ndb.StructuredProperty(Bunny, repeated=true)

class Bunny(ndb.Model):
lectureid = ndb.IntegerProperty(required=True) #identifier of lecture
    bunnyid = ndb.IntegerProperty(required=True) #unique bunny id
    creatorid = ndb.StringProperty(required=True) #identifier for creator
    rating = ndb.IntegerProperty(required=True) #note rating
    timestamp = ndb.DateTimeProperty(auto_now_add) #timestamp for sorting
    attatched_bunnies = ndb.StringProperty()
    note = ndb.TextProperty(required=True)
    
    @classmethod
    def get_lecture_bunnies(cls, lecture_key):
        return cls.query(lectureid=lecture_key)
    def get_bunny(cls, thisid):
        return cls.query(bunnyid=thisid)
    def get_user_bunnies_for_lecture(cls, lecture_key, user_key):
        return cls.query(cls, lectureid=lecture_key, creatorid=user_key)