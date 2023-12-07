import pymysql
import sys
sys.path.append('../Capstone_ThreeIdiots/DeepLearning/')
from config.DatabaseConfig import *

db = None
try:
    
    db = pymysql.connect(
        host='127.0.0.1',
        user='turtle', 
        password='capstone12345',
        db='Database',
        charset='utf8')
    
    # 테이블 생성 sql 정의
    
    sql = '''
        CREATE TABLE IF NOT EXISTS `chatbot_train_data` (
            `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
            `intent` VARCHAR(45) NULL,
            `ner` VARCHAR(1024) NULL,
            `query` TEXT NULL,
            `answer` TEXT NOT NULL,
            `answer_image` VARCHAR(2048) NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    '''
    
    sql_create_message_table = '''
        CREATE TABLE IF NOT EXISTS `message_from_server` (
            `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
            `message` TEXT NULL,
            `date` VARCHAR(45) NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    '''
    
    #테이블 생성
    with db.cursor() as cursor:
        cursor.execute(sql)
        cursor.execute(sql_create_message_table)
    db.commit()
        
except Exception as e:
        print(e)
    
finally:
    if db is not None:
        db.close()
        print("DB 연결 닫기 성공")
