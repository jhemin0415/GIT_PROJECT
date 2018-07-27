import pymysql.cursors

conn = pymysql.connect(host='localhost',
                       user='ME',
                       passwd='323411',
                       charset='utf8',
                       db = 'sakila')
cur = conn.cursor()
sql = 'select * from actor'
cur.execute(sql)
for x in cur.fetchall():
    print(x)