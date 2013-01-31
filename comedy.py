#!/usr/bin/env python

import csv
from itertools import islice
import os.path
import sqlite3

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

def main():
    subdir = 'comedy_comparisons'
    test_file = 'comedy_comparisons.test'
    test_data = os.path.join(datadir, subdir, test_file)
    data = None
    with open(test_data, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')

        print "Sample data from csv file"
        for row in take(5, data):
            print normalize(*row)

        print "Converting csv data into sqlite3..."
        with sqlite3.connect(':memory:') as conn:
            c = conn.cursor()
            c.execute("""
              CREATE TABLE preference (
                id INTEGER PRIMARY KEY,
                best TEXT,
                runnerup TEXT)
              """)
            for row in data:
                c.execute("""INSERT INTO preference (best, runnerup) VALUES (?, ?)""", normalize(*row))
            conn.commit()

if __name__ == "__main__":
    main()
