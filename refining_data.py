'''
Usage:
python refining_data.py orders.csv

While scraping the spider has shut down several times leaving corrupt rows.
The game was scraped again after relaunching the spider, but the corrupt game has left in the database.
Now we are cleaning up this duplicates

The incedents could
1) leave less number of cells in a row (and we utilise this)
2) leave the same number of rows, but a corrupt game_id (in this case the code gives a warning)
3) leave an uncorrupt line (hope that never happened), we will also check that on the later stages of cleaning the data
'''


import csv
import sys

game = []
game_id = 0

with open('refined_{}'.format(sys.argv[1]), 'wb') as orders_refined_csv:
    with open(sys.argv[1], 'rU') as orders_csv:
        orders_reader = csv.reader(orders_csv)
        orders_writer = csv.writer(orders_refined_csv)

        orders_writer.writerow(orders_reader.next())

        for row in orders_reader:
            if len(row) == 5 and row[4] != 'game_id':
                if game_id != row[4]:
                    if len(game) == 1:
                        print "Warning: Single row game", game_id, "(corrupt game_id)"
                    orders_writer.writerows(game)
                    game = []
                    game_id = row[4]
                game.append(row)
            else:
                game = []