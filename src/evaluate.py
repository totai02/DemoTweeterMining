from collections import defaultdict
import hfihu.classifier as hfihu
import nb.classifier as nb
import _thread
import json
import sys

fname = 'test.json'
test_tweet = []

hfihu_out = 'hfihu_evaluate.json'
nb_out = 'nb_evaluate.json'

count_success = 0

sumHS = defaultdict(int)
sumSi = defaultdict(int)
sumHi = defaultdict(int)

hfihu_precision = {}
hfihu_recall = {}

nb_precision = {}
nb_recall = {}

number_of_rank = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

NUMBER_THREAD = 10

busy_thread = [False for i in range(NUMBER_THREAD)]


def hfihuClassifier(id, tweet, limit):
    global count_success
    hfihu_hashtags = hfihu.classifier(tweet, limit, True)['score']
    for index in number_of_rank:
        for si in hfihu_hashtags[:index]:
            if si in tweet['hashtags']:
                sumHS[index] += 1
        sumHi[index] += index
        sumSi[index] += len(tweet['hashtags'])
    busy_thread[id] = False
    count_success += 1
    print("HF-IHU: %d tweet tested." % count_success)


def nbClassifier(id, tweet, limit):
    global count_success
    nb_hashtags = nb.classifier(tweet, limit, True)['score']
    for index in number_of_rank:
        for si in nb_hashtags[:index]:
            if si in tweet['hashtags']:
                sumHS[index] += 1
        sumHi[index] += index
        sumSi[index] += len(tweet['hashtags'])
    busy_thread[id] = False
    count_success += 1
    print("Naive Bayes: %d tweet tested." % count_success)


if __name__ == '__main__':
    with open(fname, 'r') as f:
        test_tweet = json.loads(f.readline())

        if len(sys.argv) == 1 or sys.argv[1] == 'hfihu':
            hfihu.readFile()
            count_tweet = 0
            count_success = 0
            for tweet in test_tweet:
                count_tweet += 1
                current_thread = -1
                while current_thread == -1:
                    for id_thread in range(NUMBER_THREAD):
                        if not busy_thread[id_thread]:
                            current_thread = id_thread
                            break

                try:
                    _thread.start_new_thread(hfihuClassifier, (current_thread, tweet, 100))
                    busy_thread[current_thread] = True
                except:
                    print("Error: unable to start thread")
            print(count_tweet)
            while count_tweet < count_success:
                pass

            for index in number_of_rank:
                if int(index) <= 10:
                    hfihu_precision[index] = sumHS[index] / sumSi[index]
                if int(index) >= 10 or index == 1:
                    hfihu_recall[index] = sumHS[index] / sumHi[index]

            with open(hfihu_out, 'w') as out:
                out.write(json.dumps(hfihu_precision))
                out.write("\n")
                out.write(json.dumps(hfihu_recall))

        if len(sys.argv) == 1 or sys.argv[1] == 'nb':
            nb.readFile()
            count_tweet = 0
            count_success = 0
            sumHS = defaultdict(int)
            sumSi = defaultdict(int)
            sumHi = defaultdict(int)
            for tweet in test_tweet:
                count_tweet += 1
                current_thread = -1
                while current_thread == -1:
                    for id_thread in range(NUMBER_THREAD):
                        if not busy_thread[id_thread]:
                            current_thread = id_thread
                            break
                while not busy_thread[current_thread]:
                    try:
                        _thread.start_new_thread(nbClassifier, (current_thread, tweet, 100))
                        busy_thread[current_thread] = True
                    except:
                        print("Error: unable to start thread")

            while count_tweet > count_success:
                pass

            for index in number_of_rank:
                if int(index) <= 10:
                    nb_precision[index] = sumHS[index] / sumSi[index]
                if int(index) >= 10 or index == 1:
                    nb_recall[index] = sumHS[index] / sumHi[index]

            with open(nb_out, 'w') as out:
                out.write(json.dumps(nb_precision))
                out.write("\n")
                out.write(json.dumps(nb_recall))



