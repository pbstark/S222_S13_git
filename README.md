This example uses the comedy preference data from the UC Irvine
Machine Learning Data Repository:

http://archive.ics.uci.edu/ml/datasets/YouTube+Comedy+Slam+Preference+Data

which it parses using the Python csv library:

http://docs.python.org/2/library/csv.html

It then fetches the data using Google's YouTube API python library:

https://developers.google.com/youtube/1.0/developers_guide_python

And stores the data in a sqlite3 database (simpler for the moment than
using MySQL).
