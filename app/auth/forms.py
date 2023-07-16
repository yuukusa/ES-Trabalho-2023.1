from wtforms import StringField, PasswordField, SubmitField

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp, Optional

# import email_validator
from flask_login import current_user
from wtforms import ValidationError, validators
from ..models import User


class login_form(FlaskForm):
    # email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    username = StringField(validators=[InputRequired()])
    pwd = PasswordField(validators=[InputRequired(), Length(min=5, max=72)])
    # Placeholder labels to enable form rendering
    submit_button = SubmitField("Log in")


class register_form(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(5, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(5, 72),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )
    submit_button = SubmitField("Register")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_uname(self, uname):
        if User.query.filter_by(username=uname.data).first():
            raise ValidationError("Username already taken!")
