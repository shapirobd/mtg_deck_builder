import requests
import pdb
import os

from flask import Flask, session, request, render_template, redirect, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Friendship, Message, Card, Bookmark, Deck, CardDeck, Post
from forms import LoginForm, RegisterForm


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


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global"""
    if CURR_USER_KEY in session:
        g.user = session[CURR_USER_KEY]
    else:
        g.user = None


@app.route('/')
def welcome():
    """
    If we're not logged in, show the welcome page to login/signup.
    If we are logged in, show the user's home page.
    """
    if not g.user:
        return render_template('welcome.html')
    return redirect('/home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: Renders the template for a user to login
    POST: Submits login form and signs in user if correct username & password
    """
    if g.user:
        return redirect('/home')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data, password=form.password.data)
        if user:
            db.session.add(user)
            db.session.commit(user)
            session[CURR_USER_KEY] = form.username.data
            return redirect('/home')
        flash('Username or password is incorrect', 'danger')
        return redirect('/login')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: Renders the template for a user to login
    POST: Submits register form and creates new user & logs in
    """
    if g.user:
        return redirect('/home')

    form = RegisterForm()

    if form.validate_on_submit():
        check_confirmed_pwd(form.password.data, form.confirmed_password.data)
        user = User.signup(
            username=form.username.data, password=form.password.data, email=form.email.data)
        if user:
            db.session.commit()
            session[CURR_USER_KEY] = form.username.data
            return redirect('/home')
        flash('Username or password is incorrect', 'danger')
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/home')
def show_homepage():
    cards = Card.query.all()
    return render_template('home.html', cards=cards)


def check_confirmed_pwd(pwd, confirmed_pwd):
    if pwd != confirmed_pwd:
        flash('Passwords must match - please try again.', 'danger')
        return redirect('/register')
