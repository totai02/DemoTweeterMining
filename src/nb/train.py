import json

tc = {}  # { term: count }
hc = {}  # { hashtag: count }
thc = {}  # { term: { hashtag: count } }
htc = {}  # { hashtag: { term: count } }
outFile = 'nb_data.json'
outEvaluate = 'nb_train.json'


def addTerm(term, count):
    global tc
    tc[term] = tc.get(term, 0) + count


def addHashtag(hashtag, count):
    global hc
    hc[hashtag] = hc.get(hashtag, 0) + count


def addTermHashtag(term, hashtag):
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


def writeToFile(evaluate):
    if evaluate:
        output = outEvaluate
    else:
        output = outFile
    try:
        with open(output, 'w') as f:
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