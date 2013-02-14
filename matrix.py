import csv
from itertools import islice
from logging import debug, info ,error
import os.path
import sqlite3

import gdata.youtube
import gdata.youtube.service
import numpy as np


datadir = 'Data'

def normalize(a, b, key):
	if key == 'left':
		return [a,b]
	else:
		return [b,a]

def comedy_unique_id(conn):
	subdir = 'comedy_comparisons'
	test_file = 'comedy_comparisons.train'
	test_data = os.path.join(datadir, subdir, test_file)
	data = None
	with open(test_data, 'r') as csvfile: #
	#using with it knows to close it
		data = csv.reader(csvfile, delimiter=',')
		

		print "Converting csv data into sqlite3..."
		c = conn.cursor()
		# c.execute('''WRITE SOME SQL TO DO SOMETHING''')
		c.execute("""
			CREATE TABLE com (
				id1 TEXT,
				id2 TEXT,
				bool TEXT)
				""")
		for row in data:
			c.execute("""INSERT INTO com (id1, id2) 
							 VALUES (?, ?)""", normalize(*row))
		c.execute("""SELECT * FROM com""")
		table = c.fetchall()
		print table
		conn.commit()
				#conn.close()
				#Close the connection
		c.execute("""SELECT DISTINCT(id) FROM (
	SELECT id1 AS id FROM com
UNION ALL
	SELECT id2 AS id  FROM com
)AS temp;""")
		uniq =  c.fetchall()
		label = range(1,18475)
		dic = dict(zip(uniq, label))


		


def main():
	with sqlite3.connect(':memory:') as conn: #With is gonna guarantee it's gonna close automatically
		 comedy_unique_id(conn)

if __name__ =="__main__":
	main()	