import tweepy

consumer_key = "ndGqfbZ9PX14pduPLdWvQC9Oy";

consumer_secret = "d36e8AXGCfFxGEtcVUX1ppCHFxtUVxYZSKrp5MQFpO0MFzBI16";

access_token = "3019800435-iKIwHqyjp4mxrfZHWww7xD1tTjAqCct0RP7Szhl";

access_token_secret = "cZCjQJy8HIMb9nsRPAOU6JfedXGW5qVmASrDFaYxR477s";


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
