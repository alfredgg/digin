#!/usr/bin/env python
# -*- coding: utf-8 -*-

from termcolor import cprint
from app import create_game, Deck, Card, db
from manager import import_file
from tabulate import tabulate
from os import listdir, path as ospath

pblue = lambda *x: cprint(' '.join(x), 'blue')
pred = lambda *x: cprint(' '.join(x), 'red')
pgreen = lambda *x: cprint(' '.join(x), 'green')


def create_game():
    create_game()


def list_games():
    pass


def play():
    pass


def get_console_value(prompt='> '):
    return raw_input(prompt)


def get_console_ynvalue(default='y', dprompt='> '):
    while True:
        prompt = ('[y]\\n' if default == 'y' else 'y\\[n]') + dprompt
        val = get_console_value(prompt)
        val = val if val else default
        if val in ['y', 'n']:
            return val == 'y'


def get_console_ivalue():
    while True:
        try:
            return int(get_console_value())
        except:
            continue


def choose_columns(content):
    available_columns = range(content['cols'])
    pblue('Choose first column: ', repr(available_columns))
    first = get_console_ivalue()
    del available_columns[first]
    if len(available_columns) == 1:
        second = available_columns[0]
    else:
        pblue('Choose second column: ', repr(available_columns))
        second = get_console_ivalue()
    return first, second


def choose_existent_deck():
    decks = []
    for deck in Deck.query.all():
        decks.append([deck.id, deck.name])
    if not len(decks):
        pred('Not existent decks')
        return None
    pblue('Choose an existent deck by id:')
    pblue(tabulate(decks, headers=['ID', 'NAME']))
    return Deck.query.get(get_console_ivalue())


def create_deck(name):
    deck = Deck(name=name)
    db.session.add(deck)
    db.session.commit()
    return deck

def choose_deck():
    pblue('Do you want to append data to an existent deck? ')
    val = get_console_ynvalue('n')
    deck = None
    if val:
        deck = choose_existent_deck()
    if not deck:
        pblue('New deck name')
        name = get_console_value()
        create_deck(name)
    return deck


def import_data_file(path=None, use_filename=False, positions=None):
    if not path:
        pblue('Choose path')
        path = get_console_value()
    content = import_file(path)
    if content['size'] < 1 or content['cols'] < 2:
        pred('Not enought data!')
        return
    first, second = choose_columns(content) if not positions else positions
    deck = choose_deck() if not use_filename else create_deck(ospath.splitext(ospath.basename(path))[0])
    for row in content['rows']:
        front = unicode(row[first], errors='ignore')
        rever = unicode(row[second], errors='ignore')
        deck.cards.append(Card(front=front, rever=rever))
        pgreen('Card { %s | %s } created and added to %s' % (front, rever, deck.name))
    db.session.commit()
    pblue('Data imported! :)')


def import_folder():
    pblue('Choose folder:')
    path = get_console_value()
    for filename in listdir(path):
        if filename.endswith(".csv"):
            import_data_file(ospath.join(path, filename), True, (0, 1))

def menu():
    print ''
    pblue('[1] Create new game')
    pblue('[2] List opened games')
    pblue('[3] Play game')
    pblue('[4] Import file')
    pblue('[5] Import folder')
    pblue('[0] Exit')
    value = get_console_value()
    options = {
        '0': exit,
        '1': create_game,
        '2': list_games,
        '3': play,
        '4': import_data_file,
        '5': import_folder
    }
    return options.get(value, None)

if __name__ == '__main__':
    while True:
        opt = menu()
        if opt:
            opt()