#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from datetime import datetime
import game_creator

MODE_FRONT2REVER = 0
MODE_REVER2FRONT = 1
MODE_ALTERNATE = 2

app = Flask(__name__, static_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digin.db'
db = SQLAlchemy(app)


rel_game_question = db.Table(
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    cards = db.relationship('Card', backref='deck', lazy='dynamic')


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_deck = db.Column(db.Integer,
                        db.ForeignKey('deck.id'),
                        nullable=False)
    front = db.Column(db.Text)
    rever = db.Column(db.Text)
    questions = db.relationship('Question', backref='card', lazy='dynamic')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Settings(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    questions_by_game = db.Column(db.Integer, default=10)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    mode = db.Column(db.Integer)
    error_rate = db.Column(db.Float, default=-1)
    times = db.Column(db.Integer, default=0)
    last_time = db.Column(db.DateTime)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    opened = db.Column(db.Boolean, default=True)
    date = db.Column(db.DateTime, default=datetime.now())

db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Card, methods=['GET', 'POST', 'DELETE', 'PUT'])


def mount_game(questions):
    f_questions = game_creator.extract_questions(questions)
    game = Game()


def prepare_questions(deck_id, mode):
    cards = Deck.query.get(deck_id).cards
    questions = []
    for card in cards:
        question = card.questions #.query(mode=mode)
        if question is None:
            question = Question(card=card)
            db.session.add(question)
        questions.append(question)
    db.session.commit()
    return questions


def create_game(deck_id, mode):
    questions = prepare_questions(deck_id, mode)
    return mount_game(questions)


@app.route("/new_game")
def new_game(deck_id, mode):
    game = create_game(deck_id, mode)


@app.route("/")
def hello():
    return app.send_static_file("index.html")
    return "Hello World!"

if __name__ == "__main__":
    app.run()