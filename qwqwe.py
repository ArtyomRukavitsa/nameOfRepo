from mysql.connector import connect, Error

config = { 'host':"remotemysql.com",
        'user':'JiQRuMfhFj',
        'password':'J9MyW4oGCj',
        'database':"JiQRuMfhFj"
           }
db = connect(**config)



show_table_query = "SELECT * FROM schedule"
cursor = db.cursor(True)
cursor.execute(show_table_query)
result = cursor.fetchall()
for row in result:
    print(row)