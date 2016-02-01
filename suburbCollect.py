"""
collect the suburbs in all csv files, and export the result to suburb_tb
"""

import os
import pandas as pd
import csv
import MySQLdb

count=0
searchDir="../../suburb_profiling/history_data"
suburb=[]
for file in os.listdir(searchDir):
	if file.endswith("_lot.csv") or file.endswith("_lots.csv"):
		fullPath=searchDir+'/'+file
		# df=pd.read_csv(fullPath, usecols=['Price','Project'])
		# currentSuburbs=df['Project']
		# print file
		# print df.iloc[400:405, :]

		# import pdb; pdb.set_trace()
		# print currentSuburbs
		# break
		# count=count+1
		# print count
		with open(fullPath,'rb') as csvfile:
			reader=csv.DictReader(csvfile)
			next(reader, None)
			for row in reader:
				if row!=[]: 
					currentProjectName=row['Project']
					currentSuburb=currentProjectName.split('-')[0]
					#print currentSuburb
					#count=count+1
					#import pdb; pdb.set_trace()
					if currentSuburb!=currentProjectName:
						if currentSuburb not in suburb: 
							suburb.append(currentSuburb)
					#print suburb
#import pdb; pdb.set_trace()
print len(suburb)			
###export the name of suburbs to suburb_tb
suburbSeries=pd.DataFrame({'suburb_name': suburb})
#print suburbSeries
con=MySQLdb.connect("localhost", "root", "1111", "propertyPrice_database")
cursor=con.cursor()
suburbSeries.to_sql(con=con, name='suburb_tb', if_exists='replace', flavor='mysql')
con.close()



