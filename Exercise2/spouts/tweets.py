from __future__ import absolute_import, print_function, unicode_literals

import itertools, time
import tweepy, copy
import Queue, threading

from streamparse.spout import Spout

twitter_credentials = {
    "consumer_key"        :  "ndGqfbZ9PX14pduPLdWvQC9Oy",
    "consumer_secret"     :  "d36e8AXGCfFxGEtcVUX1ppCHFxtUVxYZSKrp5MQFpO0MFzBI16",
    "access_token"        :  "3019800435-iKIwHqyjp4mxrfZHWww7xD1tTjAqCct0RP7Szhl",
    "access_token_secret" :  "cZCjQJy8HIMb9nsRPAOU6JfedXGW5qVmASrDFaYxR477s",
}

def auth_get(auth_key):
    if auth_key in twitter_credentials:
        return twitter_credentials[auth_key]
    return None

class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, listener):
        self.listener = listener
        super(self.__class__, self).__init__(listener.tweepy_api())

    def on_status(self, status):
        self.listener.queue().put(status.text, timeout = 0.01)
        return True

    def on_error(self, status_code):
        return True # keep stream alive

    def on_limit(self, track):
        return True # keep stream alive

class Tweets(Spout):

    def initialize(self, stormconf, context):
        self._queue = Queue.Queue(maxsize = 100)

        consumer_key = auth_get("consumer_key")
        consumer_secret = auth_get("consumer_secret")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        if auth_get("access_token") and auth_get("access_token_secret"):
            access_token = auth_get("access_token")
            access_token_secret = auth_get("access_token_secret")
            auth.set_access_token(access_token, access_token_secret)

        self._tweepy_api = tweepy.API(auth)

        listener = TweetStreamListener(self)

        stream = tweepy.Stream(auth, listener, timeout=None)
        stream.filter(languages=["en"], track=["a", "the", "i", "you", "u"], async=True)

    def queue(self):
        return self._queue

    def tweepy_api(self):
        return self._tweepy_api

    def next_tuple(self):
        try:
            tweet = self.queue().get(timeout = 0.1)
            if tweet:
                self.queue().task_done()
                self.emit([tweet])

        except Queue.Empty:
            self.log("Empty queue exception ")
            time.sleep(0.1)

    def ack(self, tup_id):
        pass  

    def fail(self, tup_id):
        pass 
