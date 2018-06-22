from preprocess import preprocess, stop
from collections import Counter
import json

tc = {}  # { term: count }
hc = {}  # { hashtag: count }
thc = {}  # { term: { hashtag: count } }
htc = {}  # { hashtag: { term: count } }
fname = 'worldcup.json'
outFile = 'nb_data.json'

def _addTerm(term, count):
    global tc
    tc[term] = tc.get(term, 0) + count

def _addHashtag(hashtag, count):
    global hc
    hc[hashtag] = hc.get(hashtag, 0) + count

def _addTermHashtag(term, hashtag):
    global thc, htc
    if term in thc:
        thc[term][hashtag] = thc[term].get(hashtag, 0) + 1
    else:
        hdict = {}
        hdict[hashtag] = 1
        thc[term] = hdict

    if hashtag in htc:
        htc[hashtag][term] = htc[hashtag].get(term, 0) + 1
    else:
        tdict = {}
        tdict[term] = 1
        htc[hashtag] = tdict

def _writeToFile():
    try:
        with open(outFile, 'w') as f:
            f.write(json.dumps(tc))
            f.write("\n")
            f.write(json.dumps(hc))
            f.write("\n")
            f.write(json.dumps(thc))
            f.write("\n")
            f.write(json.dumps(htc))
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
                        _addTerm(term, count_term[term])
                        _addHashtag(hashtag, count_hashtag[hashtag])
                        _addTermHashtag(term, hashtag)

        _writeToFile()