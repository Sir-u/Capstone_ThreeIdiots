import pymysql

db = None
try:
   db = pymysql.connect(
      host='127.0.0.1',
      user='root',
      password='',
      db='homestead',
      charset='utf8'
   )
   print('DB 연결 성공')

   sql = '''
   CREATE TABLE userinfo (
      uid VARCHAR(25) NOT NULL PRIMARY KEY,
      gender INT,
      age INT
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8 
   '''

   with db.cursor() as cursor:
      cursor.execute(sql)

except Exception as e:
   print(e)

finally:
   if db is not None:
      db.close()