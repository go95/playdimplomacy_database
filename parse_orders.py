"""
Usage:
python parse_orders.py orders.csv

This script reads orders from a file as yielded by the spider and decomposes it into parts:
	province -- the province with an army/fleet, which recieves the order
	order -- the order itself (e.g. MOVE)
	target -- target province (it could be destination of MOVE or province to SUPPORT/CONVOY)
	to -- additional field for SUPPORT and CONVOY orders (can be another province or "hold")
	via -- specifies if the army uses convoy intentionally.
"""

import csv
import re
import sys
order_pattern = re.compile(r'^(.*?)?([A-Z][A-Z]+)( fleet| army)?(.*?)(?:to (.*))?(VIA CONVOY)?$')

with open('parsed_{}'.format(sys.argv[1]), 'wb') as orders_write_file:
	with open(sys.argv[1]) as orders_file:
		orders_reader = csv.DictReader(orders_file)
		orders_writer = csv.DictWriter(orders_write_file,
			['game_id','date','country','province','order','target','to','via','status'])
		orders_writer.writeheader()
		for row in orders_reader:
			order_text = row['order']
			new_row = {}
			match = order_pattern.match(order_text)
			try:
				row['order'] = match.group(2)
			except:
				print row
				raise
			if row['order'] == 'BUILD':
				row['province'] = match.group(4).strip()
				row['to'] = match.group(3).strip()
			else:
				row['province'] = match.group(1)
				row['province'] = row['province'].strip() if row['province'] else ''
				row['target'] = match.group(4)
				row['target'] = row['target'].strip() if row['target'] else ''
				row['to'] = match.group(5)
				row['to'] = row['to'].strip() if row['to'] else ''
				row['via'] = match.group(6)
				row['via'] = row['via'].strip() if row['via'] else ''
			orders_writer.writerow(row)