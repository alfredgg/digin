#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from datetime import datetime

MODE_FRONT2REVER = 0
MODE_REVER2FRONT = 1
MODE_ALTERNATE = 2

app = Flask(__name__, static_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digin.db'
db = SQLAlchemy(app)


game = db.Table(
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_deck = db.Column(db.Integer, db.ForeignKey('deck.id'))
    front = db.Column(db.Text)
    rever = db.Column(db.Text)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Settings(db.Model):
    questions_by_game = db.Column(db.Integer, default=10)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    mode = db.Column(db.Integer)
    error_rate = db.Column(db.Float, default=-1)
    times = db.Column(db.Integer, default=0)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    opened = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.now())

db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Card, methods=['GET', 'POST', 'DELETE', 'PUT'])

@app.route("/new_game")
def create_game():
    pass


@app.route("/")
def hello():
    return app.send_static_file("index.html")
    return "Hello World!"

if __name__ == "__main__":
    app.run()