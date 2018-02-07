import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

with open("RegionaliSicilia.txt", "r") as file:
    fileRead = file.read()


stoplist = set('for a of the and to in'.split())
texts = [[word for word in fileRead.lower().split() if word not in stoplist]
         for document in fileRead]

from collections import defaultdict

frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [[token for token in text if frequency[token] > 1]
         for text in texts]

from pprint import pprint  # pretty-printer

pprint(texts)
