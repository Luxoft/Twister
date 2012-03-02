import MySQLdb
def runQuery(query):   
    conn = MySQLdb.connect(host="11.126.32.9", user="tsc", passwd="tsc", db="avaya")
    curs = conn.cursor()
    curs.execute(query)
