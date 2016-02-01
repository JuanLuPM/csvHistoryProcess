"""
test of dumping the dataframe data to sql tables
"""

import MySQLdb
from sqlalchemy import * 
import pandas as pd 

#con=MySQLdb.connect("localhost", "root", "1111", "propertyPrice_database")
#cursor=con.cursor()
# cursor.execute("select version()")
# data=cursor.fetchone()
# print 

engine = create_engine('mysql://root:1111@localhost:3306/mydatabase', echo=False)
connection = engine.connect()


d = {'one' : pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
  	 'two' : pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}

df=pd.DataFrame(d, index=['d','b','a'])
print df 
df.to_sql(con=connection, name='table_name_for_df', if_exists='replace', flavor='mysql', index=False)
#con.close()

##use sqlalchemy to read the data in table  "my table"
# result = engine.execute("select name from mytable")
# for row in result:
# 	print "name:", row['name']
# result.close()