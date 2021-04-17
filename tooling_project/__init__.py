from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2
import secrets

app = Flask(__name__)

ENV = "prod"

# creating the secret key
secret_key = secrets.token_hex(16)
app.config["SECRET_KEY"] = secret_key
app.config["SESSION_COOKIE_SECURE"] = False

if ENV == "dev":  # If running the app locally
    app.debug = True
    # setting the database for SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///intool"
else:  # Running the app remotely via Heroku
    app.debug = False
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgres://oopkpkqfwdwnrr:6d760123525e8dd497ed0ce41d1c48b62bef9177febe2e689204d1e3920a2220@ec2-54-242-43-231.compute-1.amazonaws.com:5432/dcn2936eotsqsl"

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

# blueprint for authenticated routes in the app
from .auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

# blueprint for the non-authenticated routes in the app
from .main import main as main_blueprint

app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run()
