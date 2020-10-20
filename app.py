import requests
import pdb
import os

import mtgsdk
import flask_paginate

# from mtgsdk import Type
from flask import Flask, session, request, render_template, redirect, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Friendship, Message, Card, Bookmark, Deck, CardDeck, Post
from forms import LoginForm, RegisterForm, TypeForm, PowerForm, ToughnessForm, DeckForm, EditUserForm
from friends import friends_blueprint
from users import users_blueprint
from bookmarks import bookmarks_blueprint
from decks import decks_blueprint
from home import home_blueprint

app = Flask(__name__)
app.register_blueprint(friends_blueprint, url_prefix="")
app.register_blueprint(users_blueprint, url_prefix="")
app.register_blueprint(bookmarks_blueprint, url_prefix="")
app.register_blueprint(decks_blueprint, url_prefix="")
app.register_blueprint(home_blueprint, url_prefix="")

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

toolbar = DebugToolbarExtension(app)

CURR_USER_KEY = 'curr-user'

TYPES = mtgsdk.Type.all()


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None
