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
from flask_login import login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
import logging
import requests
import json
from logging import Formatter, FileHandler
from .models import User
from .forms import *
from . import db


# All routes that require authentication
auth = Blueprint("auth", __name__)


# ----------------------------------------------------------------------------#
# Routes
# ----------------------------------------------------------------------------#


@auth.route("/login")
def login():
    form = LoginForm(request.form)
    return render_template("login.html", form=form)


@auth.route("/login", methods=["POST"])
def login_post():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # if this returns a user, then the email exists in the database
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check you login details and try again")
            return redirect(url_for("auth.login"))

        # If both checks pass, this is an authenticated user
        login_user(user)
        return redirect(url_for("main.dashboard"))
    else:
        print(form.errors)
        flash("There was an error with the information provided")
        return redirect(url_for("auth.login"))


@auth.route("/register")
def register():
    form = RegisterForm(request.form)
    return render_template("register.html", form=form)


@auth.route("/register", methods=["POST"])
def register_post():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        ID = form.ID.data
        email = form.email.data
        github_username = form.github_username.data
        github_token = form.github_token.data
        password = form.password.data
        confirm = form.confirm.data

        # check to see if the email is already being used
        user = User.query.filter_by(email=email).first()
        if user:  # if that email is found, redirect the user back to the register form
            flash("Email address already in use.")
            return redirect(url_for("auth.register"))

        # if the entered password and confirm match, create a new user, and hash the password
        new_user = User(
            id=ID,
            name=name,
            email=email,
            password=generate_password_hash(password, method="sha256"),
            github_username=github_username,
            github_token=github_token,
        )

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    else:
        print(form.errors)
        flash("There was an error with the information provided")
        return redirect(url_for("auth.register"))


@auth.route("/menu")
def menu():
    form = MenuForm(request.form)
    return render_template("menu.html", form=form)


@auth.route("/menu", methods=["POST"])
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
    return redirect(url_for("main.dashboard"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))
