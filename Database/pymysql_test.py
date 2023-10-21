import pymysql

db = pymysql.connect(host='localhost',
                user='root', password='0000'
                , charset='utf8')

print(db)

cursor = db.cursor()

cursor.execute('USE mydatabase')
# cursor.execute('insert into user_info(id, pwd, gender, age) values ("turtle648", 1, 25)')

cursor.execute("SELECT * FROM userinfo;")
value = cursor.fetchall()

print(value)


db.commit()
db.close()