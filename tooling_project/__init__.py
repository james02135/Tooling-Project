from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import psycopg2
import secrets
import os

app = Flask(__name__)

ENV = os.environ.get("ENV") or "prod"

# protecting the app from Cross-Site Request Forgeries (CSRF)
csrf = CSRFProtect(app)

# No longer hosting on Heroku
if ENV == "dev":  # If running the app locally
    # creating the secret key
    secret_key = secrets.token_hex(16)
    app.config["SECRET_KEY"] = secret_key
    app.config["SESSION_COOKIE_SECURE"] = False
    app.debug = True
    # setting the database for SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///intool"

# avoid SQLAlchemy warnings
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
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
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user
    return None


# blueprint for form routes in the app
from .auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

# blueprint for the page routes in the app
from .main import main as main_blueprint

app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run()
