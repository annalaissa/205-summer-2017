
import sys
import psycopg2

def main():
	conn = psycopg2.connect(database="tcount", user="w205", password="postgres", host="localhost", port="5432")

        cur = conn.cursor()

        if len(sys.argv) > 1:
             cur.execute("SELECT count FROM tweetwordcount WHERE word=%s",(sys.argv[1],))
             records = cur.fetchall()
             print 'Total number of occurrences of "' + sys.argv[1] + '":'
             print(records)
        else:
             cur.execute("SELECT * FROM tweetwordcount ORDER BY word ASC;")
             records = cur.fetchall()
             print(records)

if __name__ == "__main__":
        main()
