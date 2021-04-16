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

# All routes that don't need authentication
main = Blueprint("main", __name__)

# ----------------------------------------------------------------------------#
# Routes
# ----------------------------------------------------------------------------#


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")


@main.route("/register")
def register():
    form = RegisterForm(request.form)
    return render_template("register.html", form=form)


@main.route("/register", methods=["POST"])
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
            return redirect(url_for("main.register"))

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
        return redirect(url_for("main.home"))
    else:
        print(form.errors)
        flash("There was an error with the information provided")
        return redirect(url_for("main.register"))


@main.route("/login")
def login():
    form = LoginForm(request.form)
    return render_template("login.html", form=form)


@main.route("/login", methods=["POST"])
def login_post():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # if this returns a user, then the email exists in the database
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check you login details and try again")
            return redirect(url_for("main.login"))

        # If both checks pass, this is an authenticated user
        login_user(user)
        return redirect(url_for("auth.dashboard"))
    else:
        print(form.errors)
        flash("There was an error with the information provided")
        return redirect(url_for("main.login"))
