from tweepy.streaming import StreamListener
from datetime import datetime
from tweepy import OAuthHandler
from tweepy import Stream
import sys

tweets = 0
last_time = datetime.now()
max_tweets_per_second = 10
current_tweets = 0
hours = {}

class MyListener(StreamListener):

    def on_data(self, data):
        global tweets, last_time, current_tweets
        if str(datetime.now().hour) not in hours:
            if len(hours) > 0:
                return True
        if (datetime.now() - last_time).seconds > 0:
            current_tweets = 0
            last_time = datetime.now()
        else:
            if current_tweets >= max_tweets_per_second:
                return True
        try:
            with open('_worldcup.json', 'a') as f:
                tweets += 1
                current_tweets += 1
                print(str(tweets) + " tweet downloaded.")
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

def downloader():
    consumer_key = 'JLZAWxT74QZ4gFBhZvW1G2WUd'
    consumer_secret = 'W8qQPm82bOtJy744rZuJ52JhNsrMHzCnjXU54UEpG9oFJTtr96'
    access_token = '3236157257-CEbv8yEVjPBL4g6IZJDPAMwotsROQgTXFQoTfcF'
    access_secret = '2l0F0UEyw9BCPGdODSFuV6Gx84mAEdE3nytx6WULusmx1'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, MyListener())
    filtro = ['worldcup', '#worldcup', 'world cup', '@worldcup']
    while True:
        try:
            twitter_stream.filter(track=filtro, languages=['en'])
        except BaseException as e:
            print("Error on streaming: %s" % str(e))

if __name__ == '__main__':
    hours = sys.argv[1:]
    downloader()