from datetime import datetime
import operator
import json
import math

dataFile = "hfihu_data.json"
start_time = 0
readfile_duration = 0
classifier_duration = 0
hfm = {}
thfm = {}
corpus = 0

def _readFile():
    global hfm
    global thfm
    global corpus
    with open(dataFile, 'r') as f:
        hfm = json.loads(f.readline())
        thfm = json.loads(f.readline())
    for hashtag in hfm:
        for term in hfm[hashtag]:
            corpus += hfm[hashtag][term]



def _getHashtagOccurred(term):
    sum = 0
    for hashtag in thfm[term]:
        sum += thfm[term][hashtag]
    return sum

def _getTermOccurred(hashtag):
    sum = 0
    for term in hfm[hashtag]:
        sum += hfm[hashtag][term]
    return sum

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
    score = {}
    term_input = [term.lower() for term in argv]
    for term in term_input:
        if (term in thfm):
            for hashtag in thfm[term]:
                hf = thfm[term][hashtag] / _getHashtagOccurred(term)
                ihu = math.log2(corpus / _getTermOccurred(hashtag))
                if (hashtag in score):
                    score[hashtag] += hf * ihu
                else:
                    score[hashtag] = hf * ihu
    final_score = sorted(score.items(), key=operator.itemgetter(1), reverse=True)
    classifier_duration = datetime.now() - start_time
    for hashtag in final_score[:results]:
        print(hashtag[0])

    """ Print time: """
    print("----------------------------------")
    print("Read file duration: " + str(readfile_duration))
    print("Classifier duration: " + str(classifier_duration))
