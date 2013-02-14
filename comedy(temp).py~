#!/usr/bin/env python

import csv
import os.path
from itertools import islice
import sqlite3

import gdata.youtube
import gdata.youtube.service
temp
datadir = 'Data'

def take(n, iterable):
	"Return first n items of the iterable as a list"
	return list(islice(iterable, n))

def normalize(a, b, key):
	if key == 'left':
		return[a,b]
	else:
		return[b,a]

def convert_comedy_comparisons(conn):
	subdir = 'comedy_comparisons'
	test_file = 'comedy_comparisons.test'
	test_data = os.path.join(datadir, subdir, test_file)
	data = None
	with open(test_data, 'r') as csvfile:
		data = csv.reader(csvfile, delimiter=',')
		
		#print "Sample data from csv file"
		for row in take(5, data):
			print normalize(*row)

		print "Converting csv data into sqlite3..."
		c = conn.cursor()
		c.execute("""
			CREATE TABLE preference(
				id INTEGER PRIMARY KEY,
				best TEXT,
				runnerup TEXT)
				""")
		for row in data:
			c.execute("""INSERT INTO preference (best, runnerup)
						 VALUES (?, ?)""", normalize(*row))
		conn.commit()
		c.execute("""SELECT best, runnerup FROM preference LIMIT 5""")
		for row in c:
			print row
		## conn.close()
class ComedyComparison:
	yt_service = None

	def __init__(self):
		self.yt_service.youtube.service.YouTubeService()

	def is_better_than(best, runnerup):
		best_entry = yt_service.GetYouTubeVideoEntry(video_id=best)
		runnerup_entry = yt_service.GetYouTubeVideoEntry(video_id=runnerup)
		value = best_entry.media.title.text, "is better than", runnerup_entry.media.title.text
		return value

def main():
	with sqlite3.connect(':memory:') as conn:
		convert_comedy_comparisons(conn)

		yt_service = gdata.youtube.service.YouTubeService()

		c = conn.cursor()
		c.execute("""SELECT best, runnerup FROM preference ORDER BY RANDOM() LIMIT 5""")
		for (best, runnerup) in c:
			try:
				print comparison.is_better_than(best, runnerup)
			except gdata.service.RequestError, err:
				print err
if __name__ == "__main__":		
	main()
