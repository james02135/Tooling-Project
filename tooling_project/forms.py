from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length, Email

# Class to set the register form with the required variables
class RegisterForm(Form):
    name = StringField(
        "Name",
        validators=[
            InputRequired(message="A name is required - between 5-50 characters"),
            Length(min=5, max=50),
        ],
    )
    ID = StringField(
        "Student ID Number",
        validators=[
            DataRequired(message="A Student ID Number is required - 8 digits only"),
            Length(max=8),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            Email(
                message="An email address is required - <Student_ID_Number@mail.wit.ie"
            )
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Please enter a password - more than 6 characters"),
            EqualTo("confirm", message="Passwords must match"),
            Length(min=6),
        ],
    )
    confirm = PasswordField("Repeat Password", validators=[InputRequired()])
    github_username = StringField(
        "GitHub Username",
        validators=[InputRequired(message="A GitHub username is required")],
    )
    github_token = StringField(
        "GitHub Token",
        validators=[
            InputRequired(
                message="A GitHub token is required - xxx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            )
        ],
    )


# Class to set the login form with the required variables
class LoginForm(Form):
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


# Class to set the new project menu form with the required variables
class MenuForm(Form):
    ID = StringField("Student ID Number", validators=[DataRequired(), Length(max=8)])
    project_name = StringField("Project Name", validators=[InputRequired()])
