from collections import Counter
import json
from termpreprocess import preprocess, stop

hfm = {}
thfm = {}
corpus = 0;

def addHFM (hashtag, term, value):
    if (hashtag in hfm):
        if (term in hfm[hashtag]):
            hfm[hashtag][term] += value
        else:
            hfm[hashtag][term] = value
    else:
        terms = {}
        terms[term] = value
        hfm[hashtag] = terms

def addTHFM(term, hashtag, value):
    if (term in thfm):
        if (hashtag in thfm[term]):
            thfm[term][hashtag] += value
        else:
            thfm[term][hashtag] = value
    else:
        hashtags = {}
        hashtags[hashtag] = value
        thfm[term] = hashtags

fname = 'worldcup.json'
with open(fname, 'r') as f:
    count_hashtag = Counter()
    count_term = Counter()
    for line in f:
        if line != '\n': tweet = json.loads(line)

        # Count hashtags only
        if ('text' not in tweet): continue
        terms_hash = [term for term in preprocess(tweet['text'])
                      if term.startswith('#')]
        count_hashtag.clear()
        count_hashtag.update(terms_hash)

        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text'])
                      if term not in stop and
                      not term.startswith(('#', '@'))]
        count_term.clear()
        count_term.update(terms_only)

        corpus += len(terms_only)

        if (len(terms_hash) > 0):
            for hashtag in terms_hash:
                for term in terms_only:
                    addHFM(hashtag, term, count_term[term])
                    addTHFM(term, hashtag, count_hashtag[hashtag])


