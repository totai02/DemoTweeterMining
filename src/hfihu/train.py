from collections import defaultdict
import json

hfm = defaultdict(lambda : defaultdict(int))
thfm = defaultdict(lambda : defaultdict(int))
outFile = 'hfihu_data.json'
outEvaluate = 'hfihu_train.json'

def addHFM (hashtag, term, value):
    hfm[hashtag][term] += value


def addTHFM(term, hashtag, value):
    thfm[term][hashtag] += value


def writeToFile(evaluate):
    global corpus
    if evaluate:
        output = outEvaluate
    else:
        output = outFile
    try:
        with open(output, 'w') as f:
            f.write(json.dumps(hfm))
            f.write("\n")
            f.write(json.dumps(thfm))
    except BaseException as e:
        print("Error on_write_data: %s" % str(e))
    return True

