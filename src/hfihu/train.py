from preprocess import preprocess, stop
from collections import Counter
import json

hfm = {}
thfm = {}
fname = 'worldcup.json'
outFile = 'hfihu_data.json'

def _addHFM (hashtag, term, value):
    if (hashtag in hfm):
        if (term in hfm[hashtag]):
            hfm[hashtag][term] += value
        else:
            hfm[hashtag][term] = value
    else:
        terms = {}
        terms[term] = value
        hfm[hashtag] = terms

def _addTHFM(term, hashtag, value):
    if (term in thfm):
        if (hashtag in thfm[term]):
            thfm[term][hashtag] += value
        else:
            thfm[term][hashtag] = value
    else:
        hashtags = {}
        hashtags[hashtag] = value
        thfm[term] = hashtags

def _writeToFile():
    try:
        with open(outFile, 'w') as f:
            f.write(json.dumps(hfm))
            f.write("\n")
            f.write(json.dumps(thfm))
    except BaseException as e:
        print("Error on_write_data: %s" % str(e))
    return True

def train():
    with open(fname, 'r') as f:
        count_hashtag = Counter()
        count_term = Counter()
        for line in f:
            if line != '\n': tweet = json.loads(line)

            # Count hashtags only
            if ('text' not in tweet): continue
            terms_hash = [term for term in preprocess(tweet['text'])
                          if term.startswith('#') and len(term) > 1]
            count_hashtag.clear()
            count_hashtag.update(terms_hash)

            # Count terms only (no hashtags, no mentions)
            terms_only = [term.lower() for term in preprocess(tweet['text'])
                          if term not in stop and
                          not term.startswith(('#', '@'))]
            count_term.clear()
            count_term.update(terms_only)

            if (len(terms_hash) > 0):
                for hashtag in terms_hash:
                    for term in terms_only:
                        _addHFM(hashtag, term, count_term[term])
                        _addTHFM(term, hashtag, count_hashtag[hashtag])

        _writeToFile()


