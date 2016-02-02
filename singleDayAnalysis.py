"""analyse the date in a certain day for all suburbs
"""

#get the name of suburbs from table suburb_tb 

import MySQLdb
from sqlalchemy import *
import pandas as pd 
import intervalPricePd as intervalPrice
import numpy as np
#import subExtractionPd as subExtraction

singleDay='2016-01-20'
def priceDic2Sql(priceDic, enquirySub, connection):
	"""with the help of sqlalchemy library to import the result to database propertyPrice_database
	"""

  	pricePerUnit=priceDic[0]
  	pricePerSqm=priceDic[1]
  	pricePerChange=priceDic[2]

	#### change the data structure from dictionary to pandas dataframe type
	### the unit price
	date=np.array(pricePerUnit.items())[:,0]
	price=np.array(pricePerUnit.items())[:,1]
	#get the price for each type of property
	price2Array=np.array([np.array(x) for x in price])
	bedroom1=price2Array[:,0]
	bedroom2=price2Array[:,1]
	bedroom3=price2Array[:,2]
	bedroom4=price2Array[:,3]
	studio=price2Array[:,4]

	pricePerUnitDf=pd.DataFrame({'date':date, '1 bed': bedroom1, 
											  '2 bed': bedroom2, 
											  '3 bed': bedroom3, 
											  '4 bed': bedroom4,
											  'studio': studio })
	pricePerUnitDf['Suburb']=[enquirySub]*len(pricePerUnitDf.index)

	### the price per square

	date=np.array(pricePerSqm.items())[:,0]
	price=np.array(pricePerSqm.items())[:,1]

	#get the price for each type of property
	price2Array=np.array([np.array(x) for x in price])
	bedroom1=price2Array[:,0]
	bedroom2=price2Array[:,1]
	bedroom3=price2Array[:,2]
	bedroom4=price2Array[:,3]
	studio=price2Array[:,4]

	pricePerSqmDf=pd.DataFrame({'date':date, '1 bed': bedroom1, '2 bed': bedroom2, '3 bed': bedroom3, '4 bed': bedroom4, 'studio': studio})
	pricePerSqmDf['Suburb']=[enquirySub]*len(pricePerSqmDf.index)

	### the price of change
	date=np.array(pricePerChange.items())[:,0]
	price=np.array(pricePerChange.items())[:,1]
	#get the price for each type of property
	price2Array=np.array([np.array(x) for x in price])
	bedroom1=price2Array[:,0]
	bedroom2=price2Array[:,1]
	bedroom3=price2Array[:,2]
	bedroom4=price2Array[:,3]
	studio=price2Array[:,4]

	pricePerChangeDf=pd.DataFrame({'date':date, '1 bed': bedroom1, '2 bed': bedroom2, '3 bed': bedroom3, '4 bed': bedroom4, 'studio': studio})
	#print enquirySub
	pricePerChangeDf['Suburb']=[enquirySub]*len(pricePerChangeDf.index)

	# print pricePerUnitDf 
	# print pricePerSqmDf
	# print pricePerChangeDf
	

	


	###import the result to database propertyPrice_database
	#con=MySQLdb.connect("localhost", "root", "1111", "propertyPrice_database")
	#cursor=con.cursor()
	#import pdb; pdb.set_trace()
	pricePerUnitDf['1 bed']=pricePerUnitDf['1 bed'].map('${:,.2f}'.format)
	pricePerUnitDf['2 bed']=pricePerUnitDf['2 bed'].map('${:,.2f}'.format)
	pricePerUnitDf['3 bed']=pricePerUnitDf['3 bed'].map('${:,.2f}'.format)
	pricePerUnitDf['4 bed']=pricePerUnitDf['4 bed'].map('${:,.2f}'.format)
	pricePerUnitDf['studio']=pricePerUnitDf['studio'].map('${:,.2f}'.format)
	pricePerUnitSql=pricePerUnitDf.copy()
	#import pdb; pdb.set_trace()
	pricePerUnitSql.rename(columns={'1 bed':'one_bedroom', 
									'2 bed':'two_bedrooms', 
									'3 bed':'three_bedrooms',
									'4 bed':'four_bedrooms',
									'studio': 'studio'}, inplace=True)

	#import pdb; pdb.set_trace()
	pricePerUnitSql.to_sql(con=connection, name='price_per_unit', if_exists='append', flavor='mysql', index=False)


	pricePerSqmDf['1 bed']=pricePerSqmDf['1 bed'].map('${:,.2f}'.format)
	pricePerSqmDf['2 bed']=pricePerSqmDf['2 bed'].map('${:,.2f}'.format)
	pricePerSqmDf['3 bed']=pricePerSqmDf['3 bed'].map('${:,.2f}'.format)
	pricePerSqmDf['4 bed']=pricePerSqmDf['4 bed'].map('${:,.2f}'.format)
	pricePerSqmDf['studio']=pricePerSqmDf['studio'].map('${:,.2f}'.format)
	pricePerSqmSql=pricePerSqmDf.copy()
	#import pdb; pdb.set_trace()
	pricePerSqmSql.rename(columns={'1 bed':'one_bedroom', 
									'2 bed':'two_bedrooms', 
									'3 bed':'three_bedrooms',
									'4 bed': 'four_bedrooms',
									'studio': 'studio'}, inplace=True)
	pricePerSqmSql.to_sql(con=connection, name='price_per_sqm', if_exists='append', flavor='mysql', index=False)

	pricePerChangeDf['1 bed']=(pricePerChangeDf['1 bed']*100).map('{:,.2f}%'.format)
	pricePerChangeDf['2 bed']=(pricePerChangeDf['2 bed']*100).map('{:,.2f}%'.format)
	pricePerChangeDf['3 bed']=(pricePerChangeDf['3 bed']*100).map('{:,.2f}%'.format)
	pricePerChangeDf['4 bed']=(pricePerChangeDf['4 bed']*100).map('{:,.2f}%'.format)
	pricePerChangeDf['studio']=(pricePerChangeDf['studio']*100).map('{:,.2f}%'.format)
	pricePerChangeSql=pricePerChangeDf.copy()
	#import pdb; pdb.set_trace()
	pricePerChangeSql.rename(columns={'1 bed':'one_bedroom', 
									'2 bed':'two_bedrooms', 
									'3 bed':'three_bedrooms',
									'4 bed': 'four_bedrooms',
									'studio': 'studio'}, inplace=True)
	pricePerChangeSql.to_sql(con=connection, name='rate_of_change', if_exists='append', flavor='mysql', index=False)
	#con.close()



engine = create_engine('mysql://root:1111@localhost:3306/propertyPrice_database', echo=False)
connection = engine.connect()

suburbNameEngine=engine.execute("select suburb_name from suburb_tb")
#import pdb; pdb.set_trace()
suburbName=[]
for ind in suburbNameEngine:
	#print (ind['suburb_name'])
	suburbName.append(ind['suburb_name'])

suburbNameEngine.close()


for suburb in suburbName:
	print suburb
	# if suburb=='CONSTITUTION HILL':
	# 	import pdb; pdb.set_trace()
	staResult=intervalPrice.intervalPrice(suburb, singleDay , 1)
	priceDic2Sql(staResult, suburb, connection)


