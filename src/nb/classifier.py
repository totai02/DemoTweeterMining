from preprocess import stop
import operator
import json

dataFile = "nb_data.json"
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

def _htprob(tokens, hashtag):
    """
    Accumulates the weighted probabilities of tokens belonging to a hashtag.
    """
    p = 1
    for token in tokens:
        p *= _weightedprob(token, hashtag)
    return p

def _fprob(token, hashtag):
    """
    Calculates the probability of a token belonging to a hashtag.
    """
    if token not in thc:
        return 0
    return thc[token].get(hashtag, 0) / hc[hashtag]

def _weightedprob(token, hashtag, weight=1.0, ap=0.5):
    """
    Calculates a weighted version of _fprob() to make the classification probabilities less
    sensitive/extreme when tokens/hashtags have only been seen a small number of times.

    The weighting is applied by multiplying _fprob() with an assumed probability (ap) with a
    token weight (i.e., a weight of 2 makes the assumed probability equal to 2 tokens).
    """
    fprob = _fprob(token, hashtag)
    totals = tc.get(token, 0)
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

def _prob(tokens, hashtag):
    """
    The heart of the classifier. Uses Bayes Theorem to calculate the probability of a hashtag
    applying to a set of tokens:

                              P(Tokens|Hashtag) * P(Hashtag)
        P(Hashtag|Tokens) = ----------------------------------
                                       P(Tokens)

    which is optimised simply to:

        P(Hashtag|Tokens) =  P(Tokens|Hashtag) * P(Hashtag)
    """
    htprob = _htprob(tokens, hashtag)
    hprob = _hcount(hashtag) / _totalcount()
    return htprob * hprob


def classifier(argv, results):
    _readFile()
    probs = {}
    tokens = [term.lower() for term in argv if term not in stop]

    for hashtag in _hashtags():
        probs[hashtag] = _prob(tokens, hashtag)
    final_probs = sorted(probs.items(), key=operator.itemgetter(1))
    final_probs.reverse()
    for hashtag in final_probs[:results]:
        print(hashtag[0])
