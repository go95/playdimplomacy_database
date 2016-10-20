#drop only repetitions. What about other integrity errors

import csv
import sqlite3
import sys

conn = sqlite3.connect('database/playdiplomacy_database.db')

c = conn.cursor()

c.execute('''
CREATE TABLE games (
    last_updated     TEXT,
    GREECE_won       BOOLEAN,
    ROME_won         BOOLEAN,
    PERSIA_won       BOOLEAN,
    ENGLAND_won      BOOLEAN,
    GREECE           TEXT,
    TURKEY_won       BOOLEAN,
    FRANCE_won       BOOLEAN,
    stats            TEXT,
    EGYPT            TEXT,
    POLAND           TEXT,
    RUSSIA_won       BOOLEAN,
    AUSTRIA          TEXT,
    map_variant      TEXT,
    start            TEXT,
    BRITAIN          TEXT,
    ROME             TEXT,
    GERMANY          TEXT,
    build_deadline   TEXT,
    BRITAIN_won      BOOLEAN,
    public           TEXT,
    retreat_deadline TEXT,
    finish           TEXT,
    ITALY            TEXT,
    map_type         TEXT,
    country_choice   TEXT,
    EGYPT_won        BOOLEAN,
    USSR             TEXT,
    game_id          INTEGER PRIMARY KEY,
    variants         TEXT,
    TURKEY           TEXT,
    AUSTRIA_won      BOOLEAN,
    ENGLAND          TEXT,
    GERMANY_won      BOOLEAN,
    CARTHAGE_won     BOOLEAN,
    CARTHAGE         TEXT,
    USSR_won         BOOLEAN,
    game_type        TEXT,
    FRANCE           TEXT,
    POLAND_won       BOOLEAN,
    ITALY_won        BOOLEAN,
    PERSIA           TEXT,
    RUSSIA           TEXT,
    orders_deadline  TEXT
);
''')

c.execute('''
CREATE TABLE all_orders (
    game_id  INTEGER REFERENCES games (game_id) ON DELETE CASCADE ON UPDATE CASCADE,
    date     TEXT,
    country  TEXT,
    province TEXT,
    [order]  TEXT,
    target   TEXT,
    [to]     TEXT,
    via      TEXT,
    status   TEXT,
    PRIMARY KEY (
        game_id,
        date,
        province
    )
);
''')

c.execute('''
PRAGMA foreign_keys = 1;
''')

rotten_games = []

with open('games.csv') as games_file:
    games_reader = csv.reader(games_file)
    games_reader.next()
    for row in games_reader:
        try:
            c.execute(r'insert into games values({})'.format(', '.join([r'?']*44)),
                map(lambda x: x.decode('UTF-8'), row))
        except:
            conn.close()
            print row
            raise

with open('parsed_refined_all_orders.csv') as orders_file:
    games_reader = csv.reader(orders_file)
    games_reader.next()
    for row in games_reader:
        try:
            c.execute(r'insert into all_orders values({})'.format(', '.join([r'?']*9)),
                map(lambda x: x.decode('UTF-8'), row))
        except sqlite3.IntegrityError as e:
            if 'not unique' in str(e):
                rotten_games.append(row[0])
            else:
                conn.close()
                print row
                raise

for game in rotten_games:
    c.execute(r'DELETE FROM games WHERE game_id=?', (game,))

conn.commit()
conn.close()

# add orders as asked by Phill
# control for illegal orders
# dummy for missed orders
# 
