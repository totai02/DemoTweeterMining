from datetime import datetime
from preprocess import stop
import operator
import json
import math

dataFile = "hfihu_data.json"
hfm = {}
thfm = {}
isReaded = False


def readFile():
    global hfm
    global thfm
    global isReaded
    with open(dataFile, 'r') as f:
        hfm = json.loads(f.readline())
        thfm = json.loads(f.readline())
    isReaded = True


def _getHashtagOccurred(term):
    sum = 0
    for hashtag in thfm[term]:
        sum += thfm[term][hashtag]
    return sum


def classifier(argv, limit, evaluate = False):
    """
    Read data training
    """
    global isReaded, dataFile

    readfile_duration = 0

    if evaluate:
        dataFile = 'hfihu_train.json'

    if not isReaded:
        start_time = datetime.now()
        readFile()
        readfile_duration = datetime.now() - start_time
    """ 
    Classifier
    """
    start_time = datetime.now()
    score = {}
    term_input = [term.lower() for term in argv if term not in stop]

    for term in term_input:
        if term in thfm:
            for hashtag in thfm[term]:
                hf = thfm[term][hashtag] / _getHashtagOccurred(term)
                ihu = math.log(len(thfm) / len(hfm[hashtag]))
                score[hashtag] = score.get('hashtag', 0) + hf * ihu

    final_score = sorted(score.items(), key=operator.itemgetter(1), reverse=True)

    result_score = [hashtag[0] for hashtag in final_score[:limit]]

    classifier_duration = datetime.now() - start_time

    results = dict(score=result_score,
                   readfile_duration=readfile_duration,
                   classifier_duration=classifier_duration)

    return results
