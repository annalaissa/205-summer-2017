import sys
import psycopg2

def main():
	conn = psycopg2.connect(database="Tcount", user="postgres", password="pass", host="localhost", port="5432")

        cur = conn.cursor()

        #check if script got two arguments
        if len(sys.argv)==3:
             cur.execute("SELECT * FROM tweetwordcount WHERE count>=%s AND count<=%s",(sys.argv[1],sys.argv[2]))
             records = cur.fetchall()
             print(records)

if __name__ == "__main__":
        main()
