from preprocess import preprocess, stop
from collections import Counter
from datetime import datetime
import hfihu.train as hfihu
import nb.train as nb
import sa.train as sa
import json
import sys

method = 0
start_time = 0
totalTweet = 0
cleanTweet = 0
nonHashtag = 0
oneHashtag = 0
multiHashtag = 0
maxHashtag = 0
fname = 'worldcup.json'

if __name__ == '__main__':
    print("Trainning...")
    start_time = datetime.now()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'nb':
            method = 'nb'
        elif sys.argv[1] == 'sa':
            method = 'sa'
        else:
            method = 'hfihu'

    with open(fname, 'r') as f:
        count_hashtag = Counter()
        count_term = Counter()
        for line in f:
            if line != '\n':
                tweet = json.loads(line)
            else:
                continue

            totalTweet += 1

            if ('text' not in tweet):
                continue

            # Count hashtags only
            terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#') and len(term) > 1]
            count_hashtag.clear()
            count_hashtag.update(terms_hash)

            # Count terms only (no hashtags, no mentions)
            terms_only = [term.lower() for term in preprocess(tweet['text']) if
                          term not in stop and not term.startswith(('#', '@'))]
            count_term.clear()
            count_term.update(terms_only)

            if (len(terms_hash) == 0):
                nonHashtag += 1
                continue

            if (len(terms_hash) == 1):
                oneHashtag += 1

            if (len(terms_hash) >= 1):
                multiHashtag += 1

            if (len(terms_hash) > maxHashtag):
                maxHashtag = len(terms_hash)

            if len(terms_only) == 0:
                continue

            cleanTweet += 1

            if method == 'nb':
                for hashtag in terms_hash:
                    for term in terms_only:
                        nb.addTerm(term, count_term[term])
                        nb.addHashtag(hashtag, count_hashtag[hashtag])
                        nb.addTermHashtag(term, hashtag)
            elif method == 'sa':
                all_terms = [*terms_only, *terms_hash]
                for t1 in all_terms:
                    sa.addTerm(t1)
                    for t2 in all_terms:
                        if t1 != t2:
                            sa.addCom(t1, t2)
            else:
                for hashtag in terms_hash:
                    for term in terms_only:
                        hfihu.addHFM(hashtag, term, count_term[term])
                        hfihu.addTHFM(term, hashtag, count_hashtag[hashtag])
    if method == 'nb':
        nb.writeToFile()
    elif method == 'sa':
        sa.writeToFile(cleanTweet)
    else:
        hfihu.writeToFile()

    print("-------------------------------")
    print("Downloaded tweets:                          %d" % totalTweet)
    print("Cleaned tweets:                             %d" % cleanTweet)
    print("Tweets containing no hashtags:              %d" % nonHashtag)
    print("Tweets containing at least one hashtag:     %d" % multiHashtag)
    print("One hashtag per tweet:                      %d" % oneHashtag)
    print("Maximum number of hashtags used in a tweet: %d" % maxHashtag)
    print("Training Duration: " + str(datetime.now() - start_time))
