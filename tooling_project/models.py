from sqlalchemy.dialects.postgresql import JSON
from app_config import db

class User(db.Model):
    __tablename__ = "intool"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, id = None, name=None, email=None, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<id {}>".format(self.id)
