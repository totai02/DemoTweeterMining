from datetime import datetime
import operator
import json

dataFile = "sa_data.json"
pos_words_file = "positive-words.json"
neg_words_file = "negative-words.json"
start_time = 0
readfile_duration = 0
classifier_duration = 0
semantic_orientation = {}

def _readFile():
    global semantic_orientation
    with open(dataFile, 'r') as f:
        semantic_orientation = json.loads(f.readline())


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

    semantic_sorted = sorted(semantic_orientation.items(),
                             key=operator.itemgetter(1),
                             reverse=True)
    top_pos = semantic_sorted[:results]
    top_neg = semantic_sorted[-results:]

    """
    Print result:
    """
    print("TOP %d POSITIVE TERMS:" % results)
    for term, score in top_pos:
        print(term + ": " + str(score))
    print("----------------------------------")
    print("TOP %d NEGATIVE TERMS:" % results)
    for term, score in top_neg:
        print(term + ": " + str(score))
    print("----------------------------------")

    print("Semantic Orientation of terms:")
    for term in argv:
        print(term + ": " + str(semantic_orientation[term]))

    classifier_duration = datetime.now() - start_time
    """ Print time: """
    print("----------------------------------")
    print("Read file duration: " + str(readfile_duration))
    print("Classifier duration: " + str(classifier_duration))
