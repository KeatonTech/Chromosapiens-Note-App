from google.appengine.api import users
from models import User


def is_logged_in():
    google_user = users.get_current_user()
    if google_user:
        google_id = google_user.user_id()
        user = User.get_user(google_id=google_id)
        if user:
            return google_user
    return False