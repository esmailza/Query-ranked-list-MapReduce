#!/usr/bin/python3

from io import StringIO
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import csv
import math
import sys
import re

for line in sys.stdin:
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    for row in csv.reader(StringIO(line)):
        doc_id = row[0]
        for term in re.findall(r'[A-Za-z]+|\d+', row[1].lower().casefold()):
            if term is not "" and term.isnumeric() == False and term not in stop_words:
                stem_word = stemmer.stem(term)
                print(stem_word, doc_id, 1)
