import requests
import pdb
import os

import mtgsdk

# from mtgsdk import Type
from flask import Flask, session, request, render_template, redirect, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Friendship, Message, Card, Bookmark, Deck, CardDeck, Post
from forms import LoginForm, RegisterForm, TypeForm, PowerForm, ToughnessForm, DeckForm


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

TYPES = mtgsdk.Type.all()


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:

        user = User.query.get(session[CURR_USER_KEY])
        del session[CURR_USER_KEY]
        flash(f"Goodbye, {user.username}!")


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
    decks = Deck.query.all()

    bookmarks = Bookmark.query.all()
    bookmarked_card_ids = [bookmark.card_id for bookmark in bookmarks]
    type_form = TypeForm()
    type_form.card_type.choices = TYPES

    power_form = PowerForm()
    toughness_form = ToughnessForm()

    return render_template('home.html', cards=cards, decks=decks, type_form=type_form, power_form=power_form, toughness_form=toughness_form, bookmarked_card_ids=bookmarked_card_ids)


def check_confirmed_pwd(pwd, confirmed_pwd):
    if pwd != confirmed_pwd:
        flash('Passwords must match - please try again.', 'danger')
        return redirect('/register')


@app.route('/decks', methods=['GET', 'POST'])
def view_decks():
    decks = Deck.query.all()
    return render_template('decks.html', decks=decks)


@app.route('/decks/<int:deck_id>')
def show_deck(deck_id):
    deck = Deck.query.get(deck_id)

    bookmarks = Bookmark.query.all()
    bookmarked_card_ids = [bookmark.card_id for bookmark in bookmarks]
    type_form = TypeForm()
    type_form.card_type.choices = TYPES

    power_form = PowerForm()
    toughness_form = ToughnessForm()
    return render_template('deck.html', deck=deck, type_form=type_form, power_form=power_form, toughness_form=toughness_form, bookmarked_card_ids=bookmarked_card_ids)


@app.route('/decks/<int:deck_id>/delete', methods=['POST'])
def delete_deck(deck_id):
    deck = Deck.query.get(deck_id)
    db.session.delete(deck)
    db.session.commit()
    return redirect('/decks')


@app.route('/new', methods=['GET', 'POST'])
def create_deck():

    if g.user:
        form = DeckForm()
        form.deck_type.choices = ['Standard', 'Commander']

        if form.validate_on_submit():

            deck = Deck(deck_name=form.deck_name.data,
                        deck_type=form.deck_type.data, username=session[CURR_USER_KEY])
            db.session.add(deck)
            db.session.commit()

            return redirect('/decks')
        return render_template('new_deck.html', form=form)
    return redirect('/')


@app.route('/logout')
def logout():
    do_logout()
    return redirect('/login')


@app.route('/cards/<int:card_id>/bookmark', methods=['GET', 'POST'])
def add_bookmark(card_id):
    if g.user:
        bookmark = Bookmark(card_id=card_id, username=session[CURR_USER_KEY])
        db.session.add(bookmark)
        db.session.commit()
        return redirect('/home')
    flash('Permission denied - must be logged in to bookmark a card.')
    return redirect('/login')


@app.route('/cards/<int:card_id>/unbookmark', methods=['GET', 'POST'])
def remove_bookmark(card_id):
    if g.user:
        bookmark = Bookmark.query.filter(Bookmark.card_id == card_id).first()
        db.session.delete(bookmark)
        db.session.commit()
        return redirect('/home')
    flash('Permission denied - must be logged in to bookmark a card.')
    return redirect('/login')


@app.route('/cards/<int:card_id>/decks/<int:deck_id>', methods=['POST'])
def add_to_deck(card_id, deck_id):
    if g.user:
        card = Card.query.get(card_id)
        deck = Deck.query.get(deck_id)

        deck.cards.append(card)

        db.session.commit()
        return redirect('/home')


@app.route('/cards/<int:card_id>/decks/<int:deck_id>/delete', methods=['POST'])
def delete_from_deck(card_id, deck_id):
    if g.user:
        card_deck = CardDeck.query.filter(
            CardDeck.card_id == card_id and CardDeck.deck_id == deck_id).first()

        db.session.delete(card_deck)
        db.session.commit()

        return redirect(f'/decks/{deck_id}')
