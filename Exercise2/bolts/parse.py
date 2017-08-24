from __future__ import absolute_import, print_function, unicode_literals

import re
from streamparse.bolt import Bolt

def ascii_string(s):
  return all(ord(c) < 128 for c in s)

class ParseTweet(Bolt):

    def process(self, tup):
        tweet = tup.values[0]

        words = tweet.split()

        valid_words = []
        for word in words:

            
            if word.startswith("#"): continue
            if word.startswith("@"): continue
            if word.startswith("RT"): continue
            if word.startswith("http"): continue
            aword = word.strip("\"?><,'.:;)")
            if len(aword) > 0 and ascii_string(word):
                valid_words.append([aword])

        if not valid_words: return
        self.emit_many(valid_words)

