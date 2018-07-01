import nb.classifier
import hfihu.classifier
import sa.classifier

if __name__ == '__main__':
    print("Choose method: ")
    method = input()
    print("Enter number of result: ")
    limit = int(input())
    if method == 'sa':
        print("Enter terms list: ")
        terms = input()
        terms.replace('; ', ', ')
        print("-----------------RESULT-----------------")
        sa.classifier.classifier(terms.split(" "), limit)
    else:
        print("Enter tweet: ")
        tweet = input()
        tweet.replace('; ', ', ')
        results = {}
        if method == 'nb':
            results = nb.classifier.classifier(tweet.split(" "), limit)
        else:
            results = hfihu.classifier.classifier(tweet.split(" "), limit)

        print("-----------------RESULT-----------------")
        for hashtag in results['score']:
            print(hashtag)
        print("----------------------------------")
        print("Read file duration: " + str(results['readfile_duration']))
        print("Classifier duration: " + str(results['classifier_duration']))
