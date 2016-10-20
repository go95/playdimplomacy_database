import csv
import sqlite3
import sys

fields = [
    'last_updated',
    'GREECE_won',
    'ROME_won',
    'PERSIA_won',
    'ENGLAND_won',
    'GREECE',
    'TURKEY_won',
    'FRANCE_won',
    'stats',
    'EGYPT',
    'POLAND',
    'RUSSIA_won',
    'AUSTRIA',
    'map_variant',
    'start',
    'BRITAIN',
    'ROME',
    'GERMANY',
    'build_deadline',
    'BRITAIN_won',
    'public',
    'retreat_deadline',
    'finish',
    'ITALY',
    'map_type',
    'country_choice',
    'EGYPT_won',
    'USSR',
    'game_id',
    'variants',
    'TURKEY',
    'AUSTRIA_won',
    'ENGLAND',
    'GERMANY_won',
    'CARTHAGE_won',
    'CARTHAGE',
    'USSR_won',
    'game_type',
    'FRANCE',
    'POLAND_won',
    'ITALY_won',
    'PERSIA',
    'RUSSIA',
    'orders_deadline'
]

conn = sqlite3.connect('database/playdiplomacy_database.db')

c = conn.cursor()

c.execute(r"SELECT SUM(RUSSIA_won), SUM(GERMANY_won), SUM(TURKEY_won), SUM(ITALY_won), SUM(FRANCE_won), SUM(ENGLAND_won), SUM(AUSTRIA_won), count(*) FROM games WHERE stats = 'rank' AND map_variant = 'Standard' AND country_choice = 'rand' AND variants = 'Classic' AND game_type = 'regular'")
subsample = c.fetchall()
print subsample

c = conn.cursor()
c.execute(r"SELECT RUSSIA_won, GERMANY_won, TURKEY_won, ITALY_won, FRANCE_won, ENGLAND_won, AUSTRIA_won FROM games WHERE stats = 'rank' AND map_variant = 'Standard' AND country_choice = 'rand' AND variants = 'Classic' AND game_type = 'regular'")
subsample = c.fetchall()

results = {
    'RUSSIA': 0,
    'GERMANY': 0,
    'TURKEY': 0,
    'ITALY': 0,
    'FRANCE': 0,
    'ENGLAND': 0,
    'AUSTRIA': 0,
    'sum': 0,
}
for game in subsample:
    game = map(lambda x: 0 if x == '' else 1, game)
    if sum(game) == 1:
        results['sum'] += 1
        results['RUSSIA'] += game[0]
        results['GERMANY'] += game[1]
        results['TURKEY'] += game[2]
        results['ITALY'] += game[3]
        results['FRANCE'] += game[4]
        results['ENGLAND'] += game[5]
        results['AUSTRIA'] += game[6]

print results

c = conn.cursor()
c.execute(r"SELECT * FROM games WHERE stats = 'rank' AND map_variant = 'Standard' AND country_choice = 'rand' AND variants = 'Classic' AND game_type = 'regular'")
subsample = c.fetchall()

subsample = map(lambda x: map(lambda x: unicode(x).encode('UTF-8'), x), subsample)

with open('database/subsample.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(subsample)

conn.close()
