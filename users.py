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

users_blueprint = Blueprint('users_blueprint', __name__, static_folder='static',
                            template_folder='templates')

CURR_USER_KEY = 'curr-user'

TYPES = mtgsdk.Type.all()


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:

        user = User.query.get(session[CURR_USER_KEY])
        del session[CURR_USER_KEY]
        # flash(f"Goodbye, {user.username}!")


@users_blueprint.route('/register', methods=['GET', 'POST'])
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


@users_blueprint.route('/login', methods=['GET', 'POST'])
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
            db.session.commit()
            session[CURR_USER_KEY] = form.username.data
            return redirect('/home')
        flash('Username or password is incorrect', 'danger')
        return redirect('/login')
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
def logout():
    do_logout()
    return redirect('/login')


def check_confirmed_pwd(pwd, confirmed_pwd):
    if pwd != confirmed_pwd:
        flash('Passwords must match - please try again.', 'danger')
        return redirect('/register')


@users_blueprint.route('/users/<string:username>')
def user_profile(username):
    user = User.query.get(username)
    return render_template('user.html', user=user)


@users_blueprint.route('/users/<string:username>/edit', methods=['GET', 'POST'])
def edit_profile(username):
    if g.user:
        form = EditUserForm()
        user = User.query.get(g.user.username)

        if form.validate_on_submit():
            user.email = form.email.data
            if form.password.data == form.confirmed_password.data:
                user.password = form.password.data
            else:
                flash('Passwords do not match - please try again.', 'danger')
                return redirect(f'/users/{user.username}/edit')

            user.image_url = form.image_url.data or "/static/images/default_prof_pic.png"

            db.session.add(user)
            db.session.commit()

            return redirect('/home')

        form.email.data = user.email
        form.password.data = user.password
        form.confirmed_password.data = user.password
        form.image_url.data = user.image_url

        return render_template('edit_user.html', form=form)
    return render_template('/login')
