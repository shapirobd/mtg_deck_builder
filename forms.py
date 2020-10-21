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
    image_url = StringField('Profile Picture')


class EditUserForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8)])
    confirmed_password = PasswordField(
        "Confirm Password", validators=[InputRequired()])
    image_url = StringField('Profile Picture')


class DeckForm(FlaskForm):
    deck_name = StringField('Name', validators=[InputRequired()])
    deck_type = SelectField('Deck Type')


class TypeForm(FlaskForm):
    card_type = RadioField('Type', option_widget=CheckboxInput())


class ColorForm(FlaskForm):
    color = RadioField('Color', option_widget=CheckboxInput())


class RarityForm(FlaskForm):
    rarity = RadioField('Rarity', option_widget=CheckboxInput())


class SetForm(FlaskForm):
    set_name = RadioField('Set Name', option_widget=CheckboxInput())


class PowerForm(FlaskForm):
    power_conditionals = RadioField('Power', option_widget=CheckboxInput(),
                                    choices=["Less than", "Equal to", "Greater than"])
    power = IntegerField('Power', default=0)


class ToughnessForm(FlaskForm):

    toughness_conditionals = RadioField('Toughness', option_widget=CheckboxInput(),
                                        choices=["Less than", "Equal to", "Greater than"])
    toughness = IntegerField('Toughness', default=0)
