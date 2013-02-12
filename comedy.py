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

def convert_comedy_comparisons(conn):
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
          CREATE TABLE preference (
            id INTEGER PRIMARY KEY,
            left TEXT,
            right TEXT,
            key TEXT)
          """)
        for row in data:
            c.execute("""INSERT INTO preference (left, right, key) VALUES (?, ?, ?)""", row)
    conn.commit()
    c.execute("""SELECT left, right, key FROM preference LIMIT 5""")
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

def initialize_database(conn):
    convert_comedy_comparisons(conn)

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    dbfile = 'comedy.db'
    if not os.path.exists(dbfile):
        with sqlite3.connect(dbfile) as conn:
            initialize_database(conn)

    comparison = ComedyComparison()

    c = conn.cursor()
    c.execute("""SELECT left, right, key FROM preference ORDER BY RANDOM() LIMIT 5""")
    for (a, b, key) in c:
        try:
            print comparison.is_better_than(*normalize(a, b, key))
        except gdata.service.RequestError, err:
            error(err)

if __name__ == "__main__":
    main()
