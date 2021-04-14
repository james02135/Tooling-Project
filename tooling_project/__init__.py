from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import secrets
import os

csrf = CSRFProtect()
db = SQLAlchemy()

# Responsible for app creation

app = Flask(__name__)

# creating the secret key
secret_key = secrets.token_hex(16)
app.config["SECRET_KEY"] = secret_key
# protecting the app against Cross-Site Request Forgery (CSRF)
csrf.init_app(app)
# setting the database for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///intool"
# initialize the database
db.init_app(app)
# Login Manager authenticates the user
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)
# import the user model
from .models import User

# loads the user found via the user's ID in the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# blueprint for authenticated routes in the app
from .auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)
# blueprint for the non-authenticated routes in the app
from .main import main as main_blueprint

app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
