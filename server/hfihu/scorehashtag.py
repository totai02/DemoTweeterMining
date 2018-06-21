import sys
from termfreq import hfm, thfm, corpus
import math
from collections import Counter

def getSumFreqHashtag(term):
    sum = 0
    for hashtag in thfm[term]:
        sum += thfm[term][hashtag]
    return sum

def getSumFreqTerm(hashtag):
    sum = 0
    for term in hfm[hashtag]:
        sum += hfm[hashtag][term]
    return sum

def main(argv):
    score = {}
    for index in range(len(argv)):
        if (argv[index] in thfm):
            for hashtag in thfm[argv[index]]:
                hf = thfm[argv[index]][hashtag] / getSumFreqHashtag(argv[index])
                ihu = math.log(corpus / getSumFreqTerm(hashtag))
                if (hashtag in score):
                    score[hashtag] += hf * ihu
                else:
                    score[hashtag] = hf * ihu
    final_score = sorted(score, reverse=True)
    for hashtag in final_score:
        print(hashtag)

if __name__ == "__main__":
   main(sys.argv[1:])