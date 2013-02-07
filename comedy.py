#!/usr/bin/env python

import csv
from itertools import islice
import logging
from logging import debug, info, error
import os.path
import sqlite3

import gdata.youtube
import gdata.youtube.service

datadir = 'Data'

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def normalize(a, b, key):
    if key == 'left':
        # best
        return [a,b]
    else:
        # runnerup
        return [b,a]

def comedy_unique_id(conn):
    subdir = 'comedy_comparisons'
    test_file = 'comedy_comparisons.test'
    test_data = os.path.join(datadir, subdir, test_file)
    data = None
    with open(test_data, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')

        debug("Sample data from csv file")
        for row in take(5, data):
            debug(normalize(*row))

        info("Converting csv data into sqlite3...")
        c = conn.cursor()
        c.execute("""
          CREATE TABLE com (
            id1 TEXT,
            id2 TEXT,
            bool TEXT)
          """)
        for row in data:
            c.execute("""INSERT INTO com (id1, id2) VALUES (?, ?)""", normalize(*row))
        conn.commit()
        c.execute("""SELECT DISTINCT(id) FROM (
SELECT id1 AS id FROM com
UNION ALL
SELECT id2 AS id FROM com
) AS Temp""")
        for row in c:
            debug(row)

class ComedyComparison:
    yt_service = None

    def __init__(self):
        self.yt_service = gdata.youtube.service.YouTubeService()

    def is_better_than(self, best, runnerup):
        best_entry = self.yt_service.GetYouTubeVideoEntry(video_id=best)
        runnerup_entry = self.yt_service.GetYouTubeVideoEntry(video_id=runnerup)
        value = best_entry.media.title.text + " is better than " + runnerup_entry.media.title.text
        return value

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    with sqlite3.connect(':memory:') as conn:
        comedy_unique_id(conn)

        #comparison = ComedyComparison()

        #c = conn.cursor()
        #c.execute("""SELECT best, runnerup FROM preference ORDER BY RANDOM() LIMIT 5""")
        #for (best, runnerup) in c:
        #   try:
        #        print comparison.is_better_than(best, runnerup)
        #    except gdata.service.RequestError, err:
        #        error(err)

if __name__ == "__main__":
    main()
