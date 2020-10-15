from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import jsonify

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Friendship(db.Model):
    __tablename__ = 'friendships'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user1_username = db.Column(db.Text, db.ForeignKey(
        'users.username', ondelete="cascade"))
    user2_username = db.Column(db.Text, db.ForeignKey(
        'users.username', ondelete="cascade"))


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(25), primary_key=True,
                         unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    image_url = db.Column(db.Text)
    bookmarked_cards = db.relationship(
        'Card', secondary='bookmarks', backref='user')
    decks = db.relationship('Deck', backref='user')
    friends = db.relationship('User', secondary='friendships', primaryjoin=(
        Friendship.user1_username == username), secondaryjoin=(Friendship.user2_username == username))
    posts = db.relationship('Post', backref='user')
    messages = db.relationship(
        'Message', backref='user')

    @classmethod
    def signup(cls, username, password, email, image_url):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, password=password,
                    email=email, image_url=image_url)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return false


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    username = db.Column(db.Text, db.ForeignKey('users.username'))
    # conversation = db.relationship('Conversation', backref='messages')


# class Conversation(db.Model):
#     __tablename__ = 'conversations'

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     message_id = db.Column(db.Integer, db.ForeignKey(
#         'messages.id'))


class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    card_type = db.Column(db.Text, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    rarity = db.Column(db.Text, nullable=False)
    set_name = db.Column(db.Text, nullable=False)
    users = db.relationship('User', secondary='bookmarks', backref='cards')
    decks = db.relationship('Deck', secondary='cards_decks', backref='cards')

    @ classmethod
    def create_all_cards(cls, cards):

        for card in cards:

            colors = ' '.join(card['colors'])

            new_card = Card(name=card['name'], card_type=card['type'],
                            rarity=card['rarity'], set_name=card['setName'], colors=colors)
            db.session.add(new_card)


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.ForeignKey('users.username'))
    card_id = db.Column(db.ForeignKey('cards.id'))


class Deck(db.Model):
    __tablename__ = 'decks'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    deck_name = db.Column(db.String(30), nullable=False)
    deck_type = db.Column(db.Text, nullable=False)
    username = db.Column(db.ForeignKey('users.username'))


class CardDeck(db.Model):
    __tablename__ = 'cards_decks'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'))


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.ForeignKey('users.username'))
    content = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
