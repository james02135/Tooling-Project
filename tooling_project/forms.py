from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(Form):
    name = TextField(
        "Name", validators=[DataRequired(), Length(min=6, max=25)]
        )
    ID = TextField(
        "Student ID Number", validators=[DataRequired(), Length(min=8, max=8)]
        )
    email = TextField(
        "Email", validators=[DataRequired(), Length(min=6, max=40)]
        )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Repeat Password",
        [DataRequired(), EqualTo("Password", message="Passwords must match")],
    )


class LoginForm(Form):
    name = TextField(
        "ID Number", [DataRequired()]
        )
    password = PasswordField(
        "Password", [DataRequired()]
        )


class ForgotForm(Form):
    email = TextField(
        "Email", validators=[DataRequired(), Length(min=6, max=40)]
        )
