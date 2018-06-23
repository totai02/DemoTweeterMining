import nb.classifier
import hfihu.classifier
import sa.classifier

if __name__ == '__main__':
    print("Choose method: ")
    method = input()
    if method == 'sa':
        print("Enter terms list: ")
        terms = input()
        terms.replace('; ', ', ')
        print("-----------------RESULT-----------------")
        sa.classifier.classifier(terms.split(" "))
    else:
        print("Enter number of result: ")
        results = int(input())
        print("Enter tweet: ")
        tweet = input()
        tweet.replace('; ', ', ')
        print("-----------------RESULT-----------------")
        if method == 'nb':
            nb.classifier.classifier(tweet.split(" "), results)
        else:
            hfihu.classifier.classifier(tweet.split(" "), results)
