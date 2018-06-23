import json

hfm = {}
thfm = {}
outFile = 'hfihu_data.json'

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

def writeToFile():
    try:
        with open(outFile, 'w') as f:
            f.write(json.dumps(hfm))
            f.write("\n")
            f.write(json.dumps(thfm))
    except BaseException as e:
        print("Error on_write_data: %s" % str(e))
    return True

