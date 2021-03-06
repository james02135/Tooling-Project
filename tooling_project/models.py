from sqlalchemy.dialects.postgresql import JSON
from . import db
from flask_login import UserMixin

# User model corresponding to postgresql constraints
# UserMixin allows Flask-Login to grab the user data
class User(UserMixin, db.Model):
    __tablename__ = "intool"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))
    github_username = db.Column(db.String(120))
    github_token = db.Column(db.String(120))

    def __init__(
        self,
        id=None,
        name=None,
        email=None,
        password=None,
        github_username=None,
        github_token=None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.github_username = github_username
        self.github_token = github_token
