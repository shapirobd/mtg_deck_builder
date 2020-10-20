from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, RadioField, SelectField, FileField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import CheckboxInput, ListWidget


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8)])
    confirmed_password = PasswordField(
        "Confirm Password", validators=[InputRequired()])
    image_url = FileField('Profile Picture')


class DeckForm(FlaskForm):
    deck_name = StringField('Name', validators=[InputRequired()])
    deck_type = SelectField('Deck Type')


class TypeForm(FlaskForm):
    card_type = RadioField('Type', option_widget=CheckboxInput())


class PowerForm(FlaskForm):
    power_conditionals = RadioField('Power', option_widget=CheckboxInput(),
                                    choices=["Less than", "Equal to", "Greater than"])
    power = IntegerField('Power', default=0)


class ToughnessForm(FlaskForm):

    toughness_conditionals = RadioField('Toughness', option_widget=CheckboxInput(),
                                        choices=["Less than", "Equal to", "Greater than"])
    toughness = IntegerField('Toughness', default=0)
