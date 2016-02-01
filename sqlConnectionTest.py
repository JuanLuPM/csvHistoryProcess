"""
test the connection from python to mysql
"""

import MySQLdb
mysqlCn=MySQLdb.connect("localhost", "root", "1111", "propertyPrice_database")
cursor=mysqlCn.cursor()
cursor.execute("select version()")
data=cursor.fetchone()
print data ## get the version of MySQL 

#create an Employee table and insert one record
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
sql = """CREATE TABLE EMPLOYEE (
...          FIRST_NAME  CHAR(20) NOT NULL,
...          LAST_NAME  CHAR(20),
...          AGE INT,
...          SEX CHAR(1),
...          INCOME FLOAT )"""
cursor.execute(sql)

sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
...          LAST_NAME, AGE, SEX, INCOME)
...          VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""

cursor.execute(sql)
mysqlCn.commit()
mysqlCn.close()