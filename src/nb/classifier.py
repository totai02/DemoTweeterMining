from preprocess import stop
from datetime import datetime
import operator
import json

dataFile = "nb_data.json"
start_time = 0
readfile_duration = 0
classifier_duration = 0
tc = {}
hc = {}
thc = {}
htc = {}


def _readFile():
    global tc, hc, thc, htc
    with open(dataFile, 'r') as f:
        tc = json.loads(f.readline())
        hc = json.loads(f.readline())
        thc = json.loads(f.readline())
        htc = json.loads(f.readline())


def _htprob(terms, hashtag):
    """
    Accumulates the weighted probabilities of terms belonging to a hashtag.
    """
    p = 1
    for term in terms:
        p *= _weightedprob(term, hashtag)
    return p


def _fprob(term, hashtag):
    """
    Calculates the probability of a term belonging to a hashtag.
    """
    if term not in thc:
        return 0
    return thc[term].get(hashtag, 0) / hc[hashtag]


def _weightedprob(term, hashtag, weight=1.0, ap=0.5):
    """
    Calculates a weighted version of _fprob() to make the classification probabilities less
    sensitive/extreme when terms/hashtags have only been seen a small number of times.

    The weighting is applied by multiplying _fprob() with an assumed probability (ap) with a
    term weight (i.e., a weight of 2 makes the assumed probability equal to 2 terms).
    """
    fprob = _fprob(term, hashtag)
    totals = tc.get(term, 0)
    return ((weight * ap) + (totals * fprob)) / (weight + totals)


def _hashtags():
    """
    Returns a list of all hashtags 'seen' by the classifier.
    """
    return hc.keys()


def _hcount(hashtag):
    """
    Returns the total number of times that a hashtag has been seen.
    """
    if hashtag in hc:
        return hc[hashtag]
    return 0


def _totalcount():
    """
     Returns the total number of hashtags 'seen' by the classifier.
    """
    return len(hc)


def _prob(terms, hashtag):
    """
    The heart of the classifier. Uses Bayes Theorem to calculate the probability of a hashtag
    applying to a set of terms:

                              P(terms|Hashtag) * P(Hashtag)
        P(Hashtag|terms) = ----------------------------------
                                       P(terms)

    which is optimised simply to:

        P(Hashtag|terms) =  P(terms|Hashtag) * P(Hashtag)
    """
    htprob = _htprob(terms, hashtag)
    hprob = _hcount(hashtag) / _totalcount()
    return htprob * hprob


def classifier(argv, results):
    """
    Read data training
    """
    start_time = datetime.now()
    _readFile()
    readfile_duration = datetime.now() - start_time
    """ 
    Classifier
    """
    start_time = datetime.now()
    probs = {}
    terms = [term.lower() for term in argv if term not in stop]

    for hashtag in _hashtags():
        probs[hashtag] = _prob(terms, hashtag)
    final_probs = sorted(probs.items(), key=operator.itemgetter(1), reverse=True)
    classifier_duration = datetime.now() - start_time
    """
    Print result:
    """
    for hashtag in final_probs[:results]:
        print(hashtag[0])
    """ Print time: """
    print("----------------------------------")
    print("Read file duration: " + str(readfile_duration))
    print("Classifier duration: " + str(classifier_duration))
