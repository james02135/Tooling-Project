from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

# Class to set the register form with the required variables
class RegisterForm(Form):
    name = TextField("Name", validators=[DataRequired(), Length(min=6, max=100)])
    ID = TextField(
        "Student ID Number", validators=[DataRequired(), Length(max=8)]
    )
    email = TextField("Email", validators=[DataRequired(), Length(min=6, max=100)])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm", message="Passwords must match"),
            Length(min=6, max=40),
        ],
    )
    confirm = PasswordField("Repeat Password", validators=[DataRequired()])
    github_username = TextField("GitHub Username", validators=[DataRequired()])
    github_token = TextField("GitHub Token", validators=[DataRequired()])


# Class to set the login form with the required variables
class LoginForm(Form):
    email = TextField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


# Class to set the new project menu form with the required variables
class MenuForm(Form):
    ID = TextField(
        "Student ID Number", validators=[DataRequired(), Length(max=8)]
    )
    project_name = TextField("Project Name", validators=[DataRequired()])
