#!/usr/bin/env python

import csv
from   itertools import islice
import logging
from   logging   import debug, info, error
import os.path
import sqlite3
import sys
import getopt

import numpy
from scipy.sparse.csgraph

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
    train_file = 'comedy_comparisons.train'
    test_data = os.path.join(datadir, subdir, test_file)
    train_data = os.path.join(datadir, subdir, train_file)
    data = None
    with open(train_data, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')

        debug("Sample data from csv file")
        for row in take(5, data):
            debug(normalize(*row))

        info("Converting csv data into sqlite3...")
        c = conn.cursor()
        c.execute("""
          CREATE TABLE trainPreference (
            id INTEGER PRIMARY KEY,
            left TEXT,
            right TEXT,
            key TEXT)
          """)
        for row in data:
            c.execute("""INSERT INTO trainPreference (left, right, key) VALUES (?, ?, ?)""", row)
    conn.commit()
    c.execute("""SELECT left, right, key FROM trainPreference LIMIT 5""")
    for row in c:
        debug(row)

    c.execute("""SELECT left as "vidID" FROM trainPreference UNION SELECT right from trainPreference""")
    uniqueTrainIDs = set(c)
    debug("found " + str(len(uniqueTrainIDs)) + " unique video IDs")

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

class ComedyComparison:
    yt_service = None
    dbfile = 'comedyTrain.db'

    def __init__(self):
        self.yt_service = gdata.youtube.service.YouTubeService()

        if not os.path.exists(self.dbfile):
            with sqlite3.connect(self.dbfile) as conn:
                initialize_database(conn)
            c = conn.cursor()
            c.execute("""SELECT left, right, key FROM trainPreference ORDER BY RANDOM() LIMIT 5""")
            for (a, b, key) in c:
                try:
                    print self.is_better_than(*normalize(a, b, key))
                except gdata.service.RequestError, err:
                    error(err)

    def is_better_than(self, best, runnerup):
        best_entry = self.yt_service.GetYouTubeVideoEntry(video_id=best)
        runnerup_entry = self.yt_service.GetYouTubeVideoEntry(video_id=runnerup)
        value = best_entry.media.title.text + " is better than " + runnerup_entry.media.title.text
        return value

def initialize_database(conn):
    convert_comedy_comparisons(conn)

def main(argv=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        comparison = ComedyComparison()
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
