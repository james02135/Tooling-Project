#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from app_config import db, app
from tooling_project.models import Result, User
#from tooling_project.register import Register


# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)
    temp_name = request.form.get("name", "")
    temp_ID = request.form.get("ID", "")
    temp_email = request.form.get("email", "")
    temp_password = request.form.get("password", )
    n_message = "Please fill in your name"
    print("got here")

    # check for blanks
    if temp_name == "":
        return render_template("forms/register.html", message = n_message)
    else:
        name = temp_name

    if temp_ID == "":
        i_message = "Please fill in your Student ID Number"
        return render_template("forms/register.html", message = i_message)
    else:
        ID = temp_ID

    if temp_email == "":
        e_message = "Please fill in your email address"
        return render_template("forms/register.html", message = e_message)
    else:
        email = temp_email

    if temp_password == "":
        p_message = "Please fill in your password"
        return render_template("register.html", message = p_message)
    else:
        p_hashed = hashlib.sha256(temp_password.encode()) #hash the password the user entered
        hashed_password = p_hashed.hexdigest()

    # database insert
    host = "postgresql:///intool"
    port = "5432"
    dbname = "intool"
    user = "james"
    pw = ""
    db_conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=pw)
    db_cursor = db_conn.cursor()

    # We take the time to build our SQL query string so that
    #   (a) we can easily & quickly read it
    #   (b) we can easily & quickly edit or add/remote lines
    #   The more complex the query, the greater the benefits
    s = "INSERT INTO intool.users "
    s += "("
    s += "  name"
    s += "  ID"
    s += "  email"
    s += ", hashed_password"
    s += ") VALUES ("
    s += " '" + name + "'"
    s += " '" + ID + "'"
    s += " '" + email + "'"
    s += ",'" + hashed_password + "'"
    s += ")"
    db_cursor.execute(s)
    try:
        db_conn.commit()
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n SQL: " + s
        return render_template("register.html", message = t_message)

    t_message = "Your user account has been added."
    return render_template("register.html", message = t_message)



@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404
    if not app.debug:models
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()



