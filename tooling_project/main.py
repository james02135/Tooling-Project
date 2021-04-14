from flask import Blueprint, render_template
from flask_login import login_required, current_user

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


@main.route("/dashboard")
@login_required
def dashboard():
    # Name and ID are used as variable in the html page
    return render_template("dashboard.html", name=current_user.name, ID=current_user.id)
