# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, url_for, session, logging
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from app_config import db, app
from models import User
import hashlib


# Automatically tear down SQLAlchemy.
"""
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
"""

# Login required decorator.
"""
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
"""
# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def home():
    return render_template("pages/home.html")


@app.route("/about")
def about():
    return render_template("pages/about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    return render_template("forms/login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form['name']
        ID = request.form['ID']
        email = request.form['email']
        temp_password = request.form['password']
        p_hashed = hashlib.sha256(temp_password.encode()) #hash the entered password
        password = p_hashed.hexdigest()
        confirm = request.form['confirm']
        register = User(id = ID, name = name, email = email, password = password)
        db.session.add(register)
        db.session.commit()
        return redirect(url_for("login"))
    form = RegisterForm(request.form)
    return render_template("forms/register.html", form=form)


@app.route("/forgot")
def forgot():
    form = ForgotForm(request.form)
    return render_template("forms/forgot.html", form=form)

# ----------------------------------------------------------------------------#
# Error handlers.
# ----------------------------------------------------------------------------#

@app.errorhandler(500)
def internal_error(error):
    db_session.rollback()
    return render_template("errors/500.html"), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404
    if not app.debug:
        models
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()
