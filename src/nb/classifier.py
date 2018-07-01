from preprocess import stop
from datetime import datetime
import operator
import json

dataFile = "nb_data.json"
isReaded = False
tc = {}
hc = {}
thc = {}
htc = {}


def readFile():
    global tc, hc, thc, htc, isReaded
    with open(dataFile, 'r') as f:
        tc = json.loads(f.readline())
        hc = json.loads(f.readline())
        thc = json.loads(f.readline())
        htc = json.loads(f.readline())
    isReaded = True


def _htprob(terms, hashtag):
    p = 1
    for term in terms:
        p *= _weightedprob(term, hashtag)
    return p


def _fprob(term, hashtag):
    if term not in thc:
        return 0
    return thc[term].get(hashtag, 0) / hc[hashtag]


def _weightedprob(term, hashtag, weight=1.0, ap=0.5):
    fprob = _fprob(term, hashtag)
    totals = tc.get(term, 0)
    return ((weight * ap) + (totals * fprob)) / (weight + totals)


def _hashtags():
    return hc.keys()


def _hcount(hashtag):
    if hashtag in hc:
        return hc[hashtag]
    return 0


def _totalcount():
    return len(hc)


def _prob(terms, hashtag):
    htprob = _htprob(terms, hashtag)
    hprob = _hcount(hashtag) / _totalcount()
    return htprob * hprob


def classifier(argv, limit, evaluate = False):
    global isReaded, dataFile

    if evaluate:
        dataFile = 'nb_train.json'

    readfile_duration = 0

    if not isReaded:
        start_time = datetime.now()
        readFile()
        readfile_duration = datetime.now() - start_time

    start_time = datetime.now()
    probs = {}
    terms = [term.lower() for term in argv if term not in stop]

    for hashtag in _hashtags():
        probs[hashtag] = _prob(terms, hashtag)
    final_probs = sorted(probs.items(), key=operator.itemgetter(1), reverse=True)

    result_score = [hashtag[0] for hashtag in final_probs[:limit]]

    classifier_duration = datetime.now() - start_time

    results = dict(score=result_score,
                   readfile_duration=readfile_duration,
                   classifier_duration=classifier_duration)

    return results
