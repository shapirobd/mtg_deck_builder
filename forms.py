from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), ])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8)])
    confirmed_password = PasswordField(
        "Confirm Password", validators=[InputRequired()])
