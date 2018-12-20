import pymysql
import settings

def connect():
    connection = pymysql.connect(
        host=settings.db['host'],
        user=settings.db['login'],
        password=settings.db['password'],
        db=settings.db['db_name'],
        charset=settings.db['charset'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def create_table():
    conn = connect()
    cursor = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS """+settings.db['table_name']+""" (
    id INT AUTO_INCREMENT, 
    first_name VARCHAR(255), 
    last_name VARCHAR(255), 
    sex VARCHAR(20), 
    bdate VARCHAR(20),
    city VARCHAR(255),
    country VARCHAR(255),
    link VARCHAR(255),
    mobile_phone VARCHAR(30), 
    PRIMARY KEY (id)
    )  
    ENGINE=INNODB;"""

    cursor.execute(sql)
    conn.commit()
    conn.close()

def add_line(
        first_name,
        last_name,
        sex,
        bdate,
        mobile_phone,
        city,
        country,
        link
):
    conn = connect()
    cursor = conn.cursor()
    sql = 'INSERT INTO ' + settings.db['table_name'] + ' (first_name, last_name, sex, bdate, mobile_phone, city, country, link) VALUES ("'+first_name+'", "'+last_name+'", "'+sex+'", "'+bdate+'", "'+mobile_phone+'", "'+city+'", "'+country+'", "'+link+'")'
    cursor.execute(sql)
    conn.commit()
    conn.close()

