import requests
import pdb
import os

from flask import Flask, request, render_template, redirect, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Friendship, Message, Card, Bookmark, Deck, CardDeck, Post


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

toolbar = DebugToolbarExtension(app)

CURR_USER_KEY = 'curr-user'
