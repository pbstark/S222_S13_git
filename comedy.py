#!/usr/bin/env python

import csv
import os.path

datadir = 'Data'

def main():
    subdir = 'comedy_comparisons'
    test_file = 'comedy_comparisons.test'
    test_data = os.path.join(datadir, subdir, test_file)
    data = None
    with open(test_data, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        print data

if __name__ == "__main__":
    main()
