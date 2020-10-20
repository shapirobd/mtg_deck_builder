import requests
import pdb
import os

import mtgsdk
import flask_paginate

# from mtgsdk import Type
from app import g
from flask import Flask, session, Blueprint, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Friendship, Message, Card, Bookmark, Deck, CardDeck, Post
from forms import LoginForm, RegisterForm, TypeForm, PowerForm, ToughnessForm, DeckForm, EditUserForm

bookmarks_blueprint = Blueprint('bookmarks_blueprint', __name__, static_folder='static',
                                template_folder='templates')

CURR_USER_KEY = 'curr-user'

TYPES = mtgsdk.Type.all()


@bookmarks_blueprint.route('/cards/<int:card_id>/bookmark', methods=['GET', 'POST'])
def add_bookmark(card_id):
    if g.user:
        bookmark = Bookmark(card_id=card_id, username=session[CURR_USER_KEY])
        db.session.add(bookmark)
        db.session.commit()
        return redirect('/home')
    flash('Permission denied - must be logged in to bookmark a card.')
    return redirect('/login')


@bookmarks_blueprint.route('/cards/<int:card_id>/unbookmark', methods=['GET', 'POST'])
def remove_bookmark(card_id):
    if g.user:
        bookmark = Bookmark.query.filter(Bookmark.card_id == card_id).first()
        db.session.delete(bookmark)
        db.session.commit()
        return redirect('/home')
    flash('Permission denied - must be logged in to bookmark a card.')
    return redirect('/login')


@bookmarks_blueprint.route('/bookmarks')
def show_bookmarked_cards():
    if g.user:
        bookmarked_cards = g.user.bookmarked_cards
        decks = Deck.query.all()

        bookmarked_card_ids = [
            bookmarked_card.id for bookmarked_card in bookmarked_cards]
        type_form = TypeForm()
        type_form.card_type.choices = TYPES

        power_form = PowerForm()
        toughness_form = ToughnessForm()

        return render_template('bookmarks.html', bookmarked_cards=bookmarked_cards, decks=decks, type_form=type_form, power_form=power_form, toughness_form=toughness_form, bookmarked_card_ids=bookmarked_card_ids)
    return redirect('/login')
