#!/usr/bin/env python

import os.path

datadir = 'Data'

def main():
    subdir = 'comedy_comparisons'
    test_file = 'comedy_comparisons.test'
    print os.path.join(datadir, subdir, test_file)

if __name__ == "__main__":
    main()
