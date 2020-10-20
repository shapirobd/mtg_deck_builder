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

decks_blueprint = Blueprint('decks_blueprint', __name__, static_folder='static',
                            template_folder='templates')

CURR_USER_KEY = 'curr-user'

TYPES = mtgsdk.Type.all()


@decks_blueprint.route('/decks', methods=['GET', 'POST'])
def view_decks():
    if g.user:
        decks = g.user.decks
        return render_template('decks.html', decks=decks)


@decks_blueprint.route('/decks/<int:deck_id>')
def show_deck(deck_id):
    deck = Deck.query.get(deck_id)

    bookmarks = Bookmark.query.all()
    bookmarked_card_ids = [bookmark.card_id for bookmark in bookmarks]
    type_form = TypeForm()
    type_form.card_type.choices = TYPES

    power_form = PowerForm()
    toughness_form = ToughnessForm()
    return render_template('deck.html', deck=deck, type_form=type_form, power_form=power_form, toughness_form=toughness_form, bookmarked_card_ids=bookmarked_card_ids)


@decks_blueprint.route('/decks/<int:deck_id>/delete', methods=['POST'])
def delete_deck(deck_id):
    deck = Deck.query.get(deck_id)
    db.session.delete(deck)
    db.session.commit()
    return redirect('/decks')


@decks_blueprint.route('/new', methods=['GET', 'POST'])
def create_deck():

    if g.user:
        form = DeckForm()
        form.deck_type.choices = ['Standard', 'Commander']

        if form.validate_on_submit():

            deck = Deck(deck_name=form.deck_name.data,
                        deck_type=form.deck_type.data, username=session[CURR_USER_KEY])

            if 'card-to-add' in request.args:
                card_id = int(request.args['card-to-add'])
                card_to_add = Card.query.get(card_id)
                deck.cards.append(card_to_add)

            db.session.add(deck)
            db.session.commit()

            return redirect('/decks')
        return render_template('new_deck.html', form=form)
    return redirect('/')


@decks_blueprint.route('/cards/<int:card_id>/decks/<int:deck_id>', methods=['POST'])
def add_to_deck(card_id, deck_id):
    if g.user:
        card = Card.query.get(card_id)
        deck = Deck.query.get(deck_id)

        deck.cards.append(card)

        db.session.commit()
        return redirect('/home')


@decks_blueprint.route('/cards/<int:card_id>/decks/<int:deck_id>/delete', methods=['POST'])
def delete_from_deck(card_id, deck_id):
    if g.user:
        card_deck = CardDeck.query.filter(
            CardDeck.card_id == card_id and CardDeck.deck_id == deck_id).first()

        db.session.delete(card_deck)
        db.session.commit()

        return redirect(f'/decks/{deck_id}')


@decks_blueprint.route('/users/<string:username>/decks')
def show_users_decks(username):
    user = User.query.get(username)
    decks = user.decks
    return render_template('decks.html', decks=decks)
