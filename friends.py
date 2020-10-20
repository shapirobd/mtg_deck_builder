import requests
import pdb
import os

import mtgsdk
import flask_paginate

# from mtgsdk import Type
from app import g
from flask import Flask, Blueprint, session, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Friendship, Message, Card, Bookmark, Deck, CardDeck, Post
from forms import LoginForm, RegisterForm, TypeForm, PowerForm, ToughnessForm, DeckForm, EditUserForm

friends_blueprint = Blueprint('friends_blueprint', __name__, static_folder='static',
                              template_folder='templates')

CURR_USER_KEY = 'curr-user'

TYPES = mtgsdk.Type.all()


@friends_blueprint.route('/friends')
def show_friends():
    if g.user:
        friends = g.user.friends
        return render_template('friends.html', friends=friends)
    return redirect('/login')
