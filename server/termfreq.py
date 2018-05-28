from collections import Counter
from nltk.corpus import stopwords
from nltk import bigrams
import string
import operator
import json
import re

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

fname = 'python.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        if line != '\n': tweet = json.loads(line)
        # Create a list with all the terms
        terms_all = [term for term in preprocess(tweet['text'])]

        terms_stop = [term for term in preprocess(tweet['text']) if term.lower() not in stop]

        # Count terms only once, equivalent to Document Frequency
        terms_single = set(terms_all)
        # Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text'])
                      if term.startswith('#')]
        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text'])
                      if term not in stop and
                      not term.startswith(('#', '@'))]

        terms_bigram = bigrams(terms_stop)
        break
        # mind the ((double brackets))
        # startswith() takes a tuple (not a list) if
        # we pass a list of inputs
    print(terms_all)
    count_all.clear()
    count_all.update(terms_single)
    print(count_all.most_common(10))
    count_all.clear()
    count_all.update(terms_stop)
    print(count_all.most_common(10))
    count_all.clear()
    count_all.update(terms_hash)
    print(count_all.most_common(10))
    count_all.clear()
    count_all.update(terms_only)
    print(count_all.most_common(10))
    count_all.clear()
    count_all.update(terms_bigram)
    print(count_all.most_common(10))