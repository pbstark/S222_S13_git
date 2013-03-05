#!/usr/bin/env python
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

def clean(s,x=3):
	return str(s)[x:-x]

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
		uniq =  c.fetchall()

		dic = dict([(clean(b),a) for (a,b) in enumerate(uniq)])
		c.execute("""SELECT id1, id2, COUNT(*)
		FROM com GROUP BY id1, id2
		ORDER BY COUNT(*) DESC;""")
		#uniqpair_len = c.rowcount
		uniqpair = c.fetchall()
		#print uniqpair[1][1]

		A = lil_matrix((len(dic),len(dic)))
		# Upper triangle means rows funnier than columns; Vice versa
		for row in uniqpair:
				A[dic[row[0]],dic[row[1]]] = row[2]
		print A[0:2000,0:2000]

import networkx as nx
from matplotlib import pyplot, patches

def draw_adjacency_matrix(G, node_order=None, partitions=[], colors=[]):
    """
    - G is a netorkx graph
    - node_order (optional) is a list of nodes, where each node in G
          appears exactly once
    - partitions is a list of node lists, where each node in G appears
          in exactly one node list
    - colors is a list of strings indicating what color each
          partition should be
    If partitions is specified, the same number of colors needs to be
    specified.
    """
    adjacency_matrix = nx.to_numpy_matrix(G, dtype=np.bool, nodelist=node_order)

    #Plot adjacency matrix in toned-down black and white
    fig = pyplot.figure(figsize=(5, 5)) # in inches
    pyplot.imshow(adjacency_matrix,
                  cmap="Greys",
                  interpolation="none")

    # The rest is just if you have sorted nodes by a partition and want to
    # highlight the module boundaries
    assert len(partitions) == len(colors)
    ax = pyplot.gca()
    for partition, color in zip(partitions, colors):
        current_idx = 0
        for module in partition:
            ax.add_patch(patches.Rectangle((current_idx, current_idx),
                                          len(module), # Width
                                          len(module), # Height
                                          facecolor="none",
                                          edgecolor=color,
                                          linewidth="1"))
            current_idx += len(module)

draw_adjacency_matrix(nx.from_scipy_sparse_matrix(A))

def main():
	with sqlite3.connect('matrix.db') as conn: #With is gonna guarantee it's gonna close automatically
		 comedy_unique_id(conn)

if __name__ =="__main__":
	main()
