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
from .forms import MenuForm, RegisterForm, LoginForm
from . import db


# All routes that require authentication


# ----------------------------------------------------------------------------#
# Local Variables
# ----------------------------------------------------------------------------#


auth = Blueprint("auth", __name__)
error_message = "There was an error with the information provided"
dashboard = "main.dashboard"


# ----------------------------------------------------------------------------#
# Routes
# ----------------------------------------------------------------------------#


@auth.route("/register")
def register():
    form = RegisterForm(request.form)
    return render_template("register.html", form=form)


@auth.route("/register", methods=["POST"])
def register_post():
    form = RegisterForm(request.form)
    print(request.form)
    if form.validate_on_submit():
        name = form.name.data
        ID = form.ID.data
        email = form.email.data
        github_username = form.github_username.data
        github_token = form.github_token.data
        password = form.password.data

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
        print(request.data)
        return redirect(url_for("main.home"))
    else:
        print(form.errors)
        flash(error_message)
        return redirect(url_for("auth.register"))


@auth.route("/login")
def login():
    form = LoginForm(request.form)
    return render_template("login.html", form=form)


@auth.route("/login", methods=["POST"])
def login_post():
    form = LoginForm(request.form)
    print(request.form)
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
        print(request.data)
        flash('Logged in successfully')
        return redirect(url_for(dashboard))
    else:
        print(form.errors)
        flash(error_message)
        return redirect(url_for("auth.login"))


@auth.route("/menu")
@login_required
def menu():
    form = MenuForm(request.form)
    return render_template("menu.html", form=form)


@auth.route("/menu", methods=["POST"])
@login_required
def menu_post():
    form = MenuForm(request.form)
    print(request.form)
    if form.validate_on_submit():
        ID = form.ID.data
        project_name = form.project_name.data
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
        print(request.data)
        print(response.text)
        return redirect(url_for(dashboard))
    else:
        print(form.errors)
        flash("There was an error with the information provided")
        return redirect(url_for(dashboard))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))