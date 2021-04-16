from flask import (
    Blueprint,
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    logging,
    flash,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import logging
import requests
import json
from logging import Formatter, FileHandler
from .models import User
from .forms import MenuForm
from . import db


# All routes that require authentication
auth = Blueprint("auth", __name__)


# ----------------------------------------------------------------------------#
# Routes
# ----------------------------------------------------------------------------#


@auth.route("/menu")
@login_required
def menu():
    form = MenuForm(request.form)
    return render_template("menu.html", form=form)


@auth.route("/menu", methods=["POST"])
@login_required
def menu_post():

    ID = request.form.get("ID")
    project_name = request.form.get("project_name")
    # Retrieve the User from the database
    user = User.query.filter_by(id=ID).first()
    # Get the User's GitHub token
    token = user.github_token
    # Send the POST request to the GitHub api
    url = "https://api.github.com/user/repos"
    payload = {"name": project_name, "description": "for school", "auto_init": "true"}
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "text/plain",
        "Cookie": "_octo=GH1.1.1061749589.1617981576; logged_in=no",
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return redirect(url_for("auth.dashboard"))


@auth.route("/dashboard")
@login_required
def dashboard():
    # Name and ID are used as variable in the html page
    return render_template("dashboard.html", name=current_user.name, ID=current_user.id)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))
