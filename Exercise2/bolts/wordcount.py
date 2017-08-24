from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt

import psycopg2

class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()

    def process(self, tup):
        word = tup.values[0]

        self.counts[word] += 1
        self.emit([word, self.counts[word]])

        self.log('%s: %d' % (word, self.counts[word]))

        conn = psycopg2.connect(database="tcount", user="w205", password="postgres", host="localhost", port="5432")

        cur = conn.cursor()

        if self.counts[word] == 1:
             query = "INSERT INTO tweetwordcount VALUES (%s, 1);"
             cur.execute(query, (word,))
        else: cur.execute("UPDATE tweetwordcount SET count=%s WHERE word=%s;", (self.counts[word], word))

        conn.commit()

        conn.close()
