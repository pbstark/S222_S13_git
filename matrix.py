import csv
from itertools import islice
from logging import debug, info ,error
import os.path
import sqlite3

import gdata.youtube
import gdata.youtube.service
import numpy as np
import json, ast

from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from numpy.linalg import solve, norm
from numpy.random import rand


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
				id1 var(11),
				id2 var(11),
				bool TEXT)
				""")
		for row in data:
			c.execute("INSERT INTO com (id1, id2) VALUES (?,?)", normalize(*row))
		conn.commit()
				#conn.close()
				#Close the connection
		c.execute("""SELECT DISTINCT(id) FROM (
		SELECT id1 AS id FROM com
		UNION ALL
		SELECT id2 AS id  FROM com
		)AS temp;""")
		uniqid = []
		uniq =  c.fetchall()
		for line in uniq:
			line = str(line)
			line = line[3:-3]
			uniqid.append(line)
		#for line in uniq:
		#	line = line[2:]
		#	print line
		label = range(1,18475)
		dic = dict(zip(uniqid,label))
		c.execute("""SELECT id1, id2, COUNT(*)
		FROM com GROUP BY id1, id2
		ORDER BY COUNT(*) DESC;""")
		uniqpair = c.fetchall()
		#print uniqpair[1][1]

		A = lil_matrix((18474,18474))
		# Upper triangle means rows funnier than columns; Vice versa
		for row in range(1,358979):
				A[dic[uniqpair[row-1][0]] - 1,dic[uniqpair[row-1][1]] - 1] = uniqpair[row-1][2]
		print A[0:2000,0:2000]


		


		


def main():
	with sqlite3.connect(':memory:') as conn: #With is gonna guarantee it's gonna close automatically
		 comedy_unique_id(conn)

if __name__ =="__main__":
	main()	