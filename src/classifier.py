import nb.classifier
import hfihu.classifier

if __name__ == '__main__':
    print("Choose method: ")
    method = ""
    while True:
        method = input()
        if method != 'nb' and method != 'hfihu':
            print("Method not found!")
            continue
        break
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
