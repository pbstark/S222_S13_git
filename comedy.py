#!/usr/bin/env python

import os.path

datadir = 'Data'

def main():
    subdir = 'comedy_comparisons'
    test_file = 'comedy_comparisons.test'
    test_data = os.path.join(datadir, subdir, test_file)
    csvfile = open(test_data, 'r')
    print csvfile
    csvfile.close()
    print csvfile

if __name__ == "__main__":
    main()
