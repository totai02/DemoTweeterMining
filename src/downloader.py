from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('worldcup.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

consumer_key = 'JLZAWxT74QZ4gFBhZvW1G2WUd'
consumer_secret = 'W8qQPm82bOtJy744rZuJ52JhNsrMHzCnjXU54UEpG9oFJTtr96'
access_token = '3236157257-CEbv8yEVjPBL4g6IZJDPAMwotsROQgTXFQoTfcF'
access_secret = '2l0F0UEyw9BCPGdODSFuV6Gx84mAEdE3nytx6WULusmx1'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['worldcup'])