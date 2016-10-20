'''
Usage:
python repeated_entries.py orders.csv

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

orders_set = set()

with open(sys.argv[1], 'rU') as orders_csv:
    orders_reader = csv.reader(orders_csv)

    for row in orders_reader:
        ident = (row[0], row[1], row[3])
        if ident in orders_set:
            print ident
        else:
            orders_set.add(ident)

