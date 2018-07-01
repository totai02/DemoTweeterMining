from collections import defaultdict
import math
import json

tc = {}
com = {}
t_probs = {}
com_probs = defaultdict(lambda : defaultdict(int))

outFile = 'sa_data.json'
pos_words_file = "positive-words.json"
neg_words_file = "negative-words.json"


def addTerm(term):
    global tc
    tc[term] = tc.get(term, 0) + 1

def addCom(term1, term2):
    global com
    if term1 in com:
        com[term1][term2] = com[term1].get(term2, 0) + 1
    else:
        t_dict = {}
        t_dict[term2] = 1
        com[term1] = t_dict

def writeToFile(tweets: int):
    with open(pos_words_file, 'r') as f:
        positive_vocab = json.loads(f.readline())
    with open(neg_words_file, 'r') as f:
        negative_vocab = json.loads(f.readline())

    t_vocab = [*positive_vocab, *negative_vocab]

    for term in com.keys():
        t_probs[term] = tc[term] / tweets
        for vocab in t_vocab:
            if com[term].get(vocab, 0) != 0:
                com_probs[term][vocab] = com[term][vocab] / tweets

    pmi = defaultdict(lambda: defaultdict(int))
    for t1 in com_probs:
        for t2 in com_probs[t1]:
            denom = t_probs[t1] * t_probs[t2]
            pmi[t1][t2] = math.log2(com_probs[t1][t2] / denom)

    semantic_orientation = {}
    for term, n in t_probs.items():
        positive_assoc = sum(pmi[term][tx] for tx in positive_vocab if tx in pmi[term])
        negative_assoc = sum(pmi[term][tx] for tx in negative_vocab if tx in pmi[term])
        semantic_orientation[term] = positive_assoc - negative_assoc

    try:
        with open(outFile, 'w') as f:
            f.write(json.dumps(semantic_orientation))
    except BaseException as e:
        print("Error on_write_data: %s" % str(e))
    return True


