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
from forms import LoginForm, RegisterForm, TypeForm, PowerForm, ToughnessForm, DeckForm, EditUserForm, ColorForm, RarityForm, SetForm

home_blueprint = Blueprint('home_blueprint', __name__, static_folder='static',
                           template_folder='templates')

CURR_USER_KEY = 'curr-user'

TYPES = mtgsdk.Type.all()
SETS = [mtg_set.name for mtg_set in mtgsdk.Set.all()]
RARITIES = ['Common', 'Uncommon', 'Rare', 'Mythic Rare']
COLORS = ['White', 'Blue', 'Black', 'Green', 'Red']


@ home_blueprint.route('/')
def welcome():
    """
    If we're not logged in, show the welcome page to login/signup.
    If we are logged in, show the user's home page.
    """
    if not g.user:
        return render_template('welcome.html')

    return redirect('/home')


@ home_blueprint.route('/home')
def show_homepage():

    page = 1
    if 'page' in request.args:
        page = int(request.args['page'])

    base_url = '/home?'

    first_card_id = ((page-1)*100) + 1
    last_card_id = (page*100) + 1
    id_range = range(first_card_id, last_card_id)

    cards = Card.query.filter(Card.id.in_(id_range)).all()

    decks = Deck.query.all()

    bookmarks = Bookmark.query.all()
    bookmarked_card_ids = [bookmark.card_id for bookmark in bookmarks]

    type_form = TypeForm()
    type_form.card_type.choices = TYPES

    color_form = ColorForm()
    color_form.color.choices = COLORS

    rarity_form = RarityForm()
    rarity_form.rarity.choices = RARITIES

    set_form = SetForm()
    set_form.set_name.choices = SETS

    power_form = PowerForm()
    toughness_form = ToughnessForm()

    # resp = requests.get('http://api.magicthegathering.io/v1/cards', {
    #     'key': "$2a$10$TNyqKQQQSzVjgGXY87waZuBIKAS78.NkY2o.H004TfBU.eISv.Pt6"})

    # first = resp.links['first']
    # last = resp.links['last']

    return render_template('home.html', base_url=base_url, page=page, cards=cards, decks=decks, type_form=type_form, power_form=power_form, toughness_form=toughness_form, color_form=color_form, rarity_form=rarity_form,
                           set_form=set_form, bookmarked_card_ids=bookmarked_card_ids)


@ home_blueprint.route('/home/search')
def search():

    args = request.args
    term = request.args['term']
    category = request.args['category']

    base_url = f'/home/search?term={term}&category={category}&'

    if category == 'card':

        page = 1

        if 'page' in request.args:
            page = int(request.args['page'])

        first_card_index = ((page-1)*100) + 1
        last_card_index = (page*100) + 1
        index_range = range(first_card_index, last_card_index)

        all_cards = Card.query.filter(
            Card.name.ilike(f'%{term}%')).all()

        cards = [card for card in all_cards if (all_cards.index(
            card) + 1) in index_range]

        decks = Deck.query.all()

        bookmarks = Bookmark.query.all()
        bookmarked_card_ids = [bookmark.card_id for bookmark in bookmarks]

        type_form = TypeForm()
        type_form.card_type.choices = TYPES

        color_form = ColorForm()
        color_form.card_type.choices = COLORS

        rarity_form = RarityForm()
        rarity_form.card_type.choices = RARITIES

        set_form = SetForm()
        set_form.card_type.choices = SETS

        power_form = PowerForm()
        toughness_form = ToughnessForm()

        return render_template('home.html', base_url=base_url, page=page, cards=cards, decks=decks, type_form=type_form,
                               power_form=power_form, toughness_form=toughness_form, color_form=color_form, rarity_form=rarity_form,
                               set_form=set_form, bookmarked_card_ids=bookmarked_card_ids)

    elif category == 'deck':
        decks = Deck.query.filter(
            (Deck.deck_name.ilike(f'%{term}%')) | (
                Deck.deck_type.ilike(f'%{term}%'))).all()
        return render_template('decks.html', decks=decks)

    elif category == 'friend':
        friends = [friend for friend in User.friends if friend.name == term]
        return render_template('friends.html', friends=friends)
