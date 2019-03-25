from frontend import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(127))
    email = db.Column(db.String(127))
    auth_token = db.Column(db.String(255))

    def __init__(self, id, name, email, auth_token):
        self.user_id = id
        self.name = name
        self.email = email
        self.auth_token = auth_token
