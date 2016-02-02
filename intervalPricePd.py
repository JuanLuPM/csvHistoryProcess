"""
search the *.csv files to get the price result in a certain period, and output the result to output.csv
"""

import dateutil.parser as dparser
import datetime
import csv 
from suburbExtraction import * 
import os.path
import sys
#import collections
import numpy as np
#import optparse
import argparse
import pandas as pd 
import MySQLdb


fileDir='/Users/juanlu/Workspace/suburb_profiling/history_data/'

def intervalPrice(enquirySub, startDate, interval, statusCheck=None):
	##extract the year, month and date
	startPoint=dparser.parse(startDate,fuzzy=True)

	#endPoint=startPoint-datetime.timedelta(days=20)

	#get the date list
	#print startPoint
	daysList=[startPoint-datetime.timedelta(days=x) for x in range(0, interval)]
	#print daysList

	#import pdb; pdb.set_trace()
	priceUnitDic={}
	priceSqmDic={}
	priceChangeDic={}
	
	for days in daysList:
		# currentDay=days.timetuple()
		# year=currentDay[0]
		# month=currentDay[1]
		# date=currentDay[2]

		# currentYear=days.year
		# currentMonth=days.month.strftime(%m)
		# currentDate=days.day
		currentDate=days.strftime('%Y_%m_%d')
		#check the format

		
		#print currentDate
		#create the csv file name
		# fileName=str(year)+'_'+str(month)+'_'+str(date)+'_'+'lots.csv'
		fileName=currentDate+'_lots.csv'
		fileFullPath=fileDir+fileName

		if os.path.isfile(fileFullPath):
			#print fileFullPath
			#print currentDate

			if statusCheck==True:
				statusCheck='a'
			else:
				statusCheck=None
			currentPrice=suburbExtraction(enquirySub, fileFullPath, statusCheck)
			if currentPrice!=None:
				#print currentPrice
				priceUnitDic[days]=currentPrice['price per unit']
				priceSqmDic[days]=currentPrice['price per sqm']
				# if ind!=0: #calculate the rate of change
				# 	dayAfter=days+datetime.timedelta(days=1)
				# 	priceAfter=priceUnitDic[dayAfter]
				# 	priceCurrentDay=currentPrice['price per unit']
				# 	priceChange=np.divide((np.array(priceAfter)-np.array(priceCurrentDay)), np.array(priceCurrentDay) )
				#	priceChangeDic[dayAfter]=priceChange
					# print np.array(priceAfter)
					# print np.array(priceCurrentDay)
					# print priceChange
					#import pdb; pdb.set_trace()
				#print priceUnitDic,priceSqmDic
		#ind=ind+1
	
	###calculate the rate of change of price per unit
	
	#sortedPriceUnitDic=collections.OrderedDict(sorted(priceUnitDic.items(),reverse=True))
	ind=0
	for key, value in sorted(priceUnitDic.iteritems(), reverse=True):

		if ind!=0:
			#dayAfter=key+datetime.timedelta(days=1)
			priceCurrent=value
			#priceAfter=priceUnitDic[dayAfter]
			priceChange=np.divide(np.array(priceAfter)-np.array(priceCurrent), np.array(priceCurrent))
			priceChangeDic[dayAfter]=priceChange
		dayAfter=key
		priceAfter=value
		ind=ind+1

	priceChangeDic[dayAfter]=[0,0,0,0,0]
	#import pdb; pdb.set_trace()
	return [priceUnitDic, priceSqmDic, priceChangeDic]			

    # if (os.path.isfile(fileFullPath)==Ture):
    # 	print currentDate
		#suburbExtraction(enquirySub, fileFullPath)

	# print fileFullPath

	# f=open(fileFullPath, 'rb')

	# print f
	# f.close()
	#break
def priceDic2csv(priceDic, enquirySub):
	"""put the data in priceDic to result.csv 
	"""
  	pricePerUnit=priceDic[0]
  	pricePerSqm=priceDic[1]
  	pricePerChange=priceDic[2]

  	 #print pricePerUnit
  	 #print pricePerSqm 

 #  	outputFile=open('output.csv', 'w')
 #  	writer=csv.writer(outputFile)
	# writer.writerow(["price per unit"])
	# writer.writerow([ None,'1 bedroom', '2 bedrooms','3 bedrooms' ])
	# for key, value in sorted(pricePerUnit.iteritems(), reverse=True):
	# 	writer.writerow([key.strftime("%y/%m/%d"), '${:,.2f}'.format(value[0]), '${:,.2f}'.format(value[1]), '${:,.2f}'.format(value[2])])

	# writer.writerow([])	
	# writer.writerow(["price per sqm"])
	# writer.writerow([ None,'1 bedroom', '2 bedrooms','3 bedrooms' ])
	# for key, value in sorted(pricePerSqm.iteritems(), reverse=True):
	# 	writer.writerow([key.strftime("%y/%m/%d"), '${:,.2f}'.format(value[0]), '${:,.2f}'.format(value[1]), '${:,.2f}'.format(value[2])])

	# writer.writerow([])
	# writer.writerow(["rate of change"])
	# writer.writerow([ None,'1 bedroom', '2 bedrooms','3 bedrooms' ])
	# for key, value in sorted(pricePerChange.iteritems(), reverse=True):
	# 	writer.writerow([key.strftime("%y/%m/%d"), '{:,.2f}%'.format(value[0]*100), '{:,.2f}%'.format(value[1]*100), '{:,.2f}%'.format(value[2]*100)])

	# use pandas dataframe type to write csv file
	#### change the data structure from dictionary to dataframe
	### the unit price
	date=np.array(pricePerUnit.items())[:,0]
	price=np.array(pricePerUnit.items())[:,1]
	#get the price for each type of property
	price2Array=np.array([np.array(x) for x in price])
	bedroom1=price2Array[:,0]
	bedroom2=price2Array[:,1]
	bedroom3=price2Array[:,2]

	pricePerUnitDf=pd.DataFrame({'date':date, '1 bed': bedroom1, '2 bed': bedroom2, '3 bed': bedroom3})
	pricePerUnitDf['Suburb']=[enquirySub]*len(pricePerUnitDf.index)

	### the price per square
	date=np.array(pricePerSqm.items())[:,0]
	price=np.array(pricePerSqm.items())[:,1]
	#get the price for each type of property
	price2Array=np.array([np.array(x) for x in price])
	bedroom1=price2Array[:,0]
	bedroom2=price2Array[:,1]
	bedroom3=price2Array[:,2]

	pricePerSqmDf=pd.DataFrame({'date':date, '1 bed': bedroom1, '2 bed': bedroom2, '3 bed': bedroom3})
	pricePerSqmDf['Suburb']=[enquirySub]*len(pricePerSqmDf.index)

	### the price of change
	date=np.array(pricePerChange.items())[:,0]
	price=np.array(pricePerChange.items())[:,1]
	#get the price for each type of property
	price2Array=np.array([np.array(x) for x in price])
	bedroom1=price2Array[:,0]
	bedroom2=price2Array[:,1]
	bedroom3=price2Array[:,2]

	pricePerChangeDf=pd.DataFrame({'date':date, '1 bed': bedroom1, '2 bed': bedroom2, '3 bed': bedroom3})
	#print enquirySub
	pricePerChangeDf['Suburb']=[enquirySub]*len(pricePerChangeDf.index)

	print pricePerUnitDf 
	print pricePerSqmDf
	print pricePerChangeDf
	#import pdb; pdb.set_trace()

	
	#####write result to csv files
 	outputFile=open('output.csv', 'w')
  	writer=csv.writer(outputFile)
	
	writer.writerow(["price per unit"])
	#pricePerUnitDf.Options.display.foloat_format='${:,.2f}'.format

	pricePerUnitDf['1 bed']=pricePerUnitDf['1 bed'].map('${:,.2f}'.format)
	pricePerUnitDf['2 bed']=pricePerUnitDf['2 bed'].map('${:,.2f}'.format)
	pricePerUnitDf['3 bed']=pricePerUnitDf['3 bed'].map('${:,.2f}'.format)
	pricePerUnitDf.rename(columns={'1 bed':'1 bedroom', '2 bed':'2 bedrooms', '3 bed':'3 bedrooms'}, inplace=True)
	pricePerUnitDf.to_csv(outputFile, columns=['date','1 bedroom', '2 bedrooms', '3 bedrooms'], index=False)
	writer.writerow([])

	writer.writerow(["price per sqm"])
	pricePerSqmDf['1 bed']=pricePerSqmDf['1 bed'].map('${:,.2f}'.format)
	pricePerSqmDf['2 bed']=pricePerSqmDf['2 bed'].map('${:,.2f}'.format)
	pricePerSqmDf['3 bed']=pricePerSqmDf['3 bed'].map('${:,.2f}'.format)
	pricePerSqmDf.rename(columns={'1 bed':'1 bedroom', '2 bed':'2 bedrooms', '3 bed':'3 bedrooms'}, inplace=True)
	pricePerSqmDf.to_csv(outputFile, columns=['date','1 bedroom', '2 bedrooms', '3 bedrooms'], index=False)
	writer.writerow([])

	writer.writerow(["rate of change"])
	pricePerChangeDf['1 bed']=(pricePerChangeDf['1 bed']*100).map('{:,.2f}%'.format)
	pricePerChangeDf['2 bed']=(pricePerChangeDf['2 bed']*100).map('{:,.2f}%'.format)
	pricePerChangeDf['3 bed']=(pricePerChangeDf['3 bed']*100).map('{:,.2f}%'.format)

	pricePerChangeDf.rename(columns={'1 bed':'1 bedroom', '2 bed':'2 bedrooms', '3 bed':'3 bedrooms'}, inplace=True)
	pricePerChangeDf.to_csv(outputFile, columns=['date','1 bedroom', '2 bedrooms', '3 bedrooms'], index=False)

	outputFile.close()


	# ###import the result to database propertyPrice_database
	# con=MySQLdb.connect("localhost", "root", "1111", "propertyPrice_database")
	# cursor=con.cursor()
	
	# pricePerUnitSql=pricePerUnitDf.copy()
	# #import pdb; pdb.set_trace()
	# pricePerUnitSql.rename(columns={'1 bedroom':'one_bedroom', '2 bedrooms':'two_bedrooms', '3 bedrooms':'three_bedrooms'}, inplace=True)
	# pricePerUnitSql.to_sql(con=con, name='price_per_unit', if_exists='append', flavor='mysql', index=False)

	# pricePerSqmSql=pricePerSqmDf.copy()
	# #import pdb; pdb.set_trace()
	# pricePerSqmSql.rename(columns={'1 bedroom':'one_bedroom', '2 bedrooms':'two_bedrooms', '3 bedrooms':'three_bedrooms'}, inplace=True)
	# pricePerSqmSql.to_sql(con=con, name='price_per_sqm', if_exists='append', flavor='mysql', index=False)

	# pricePerChangeSql=pricePerChangeDf.copy()
	# #import pdb; pdb.set_trace()
	# pricePerChangeSql.rename(columns={'1 bedroom':'one_bedroom', '2 bedrooms':'two_bedrooms', '3 bedrooms':'three_bedrooms'}, inplace=True)
	# pricePerChangeSql.to_sql(con=con, name='rate_of_change', if_exists='append', flavor='mysql', index=False)
	# con.close()


def priceDic2Sql(priceDic, enquirySub):
	"""put the data in priceDic to MySQL database propertyPrice_database
	"""
  	pricePerUnit=priceDic[0]
  	pricePerSqm=priceDic[1]
  	pricePerChange=priceDic[2]

  	 #print pricePerUnit
  	 #print pricePerSqm 

 #  	outputFile=open('output.csv', 'w')
 #  	writer=csv.writer(outputFile)
	# writer.writerow(["price per unit"])
	# writer.writerow([ None,'1 bedroom', '2 bedrooms','3 bedrooms' ])
	# for key, value in sorted(pricePerUnit.iteritems(), reverse=True):
	# 	writer.writerow([key.strftime("%y/%m/%d"), '${:,.2f}'.format(value[0]), '${:,.2f}'.format(value[1]), '${:,.2f}'.format(value[2])])

	# writer.writerow([])	
	# writer.writerow(["price per sqm"])
	# writer.writerow([ None,'1 bedroom', '2 bedrooms','3 bedrooms' ])
	# for key, value in sorted(pricePerSqm.iteritems(), reverse=True):
	# 	writer.writerow([key.strftime("%y/%m/%d"), '${:,.2f}'.format(value[0]), '${:,.2f}'.format(value[1]), '${:,.2f}'.format(value[2])])

	# writer.writerow([])
	# writer.writerow(["rate of change"])
	# writer.writerow([ None,'1 bedroom', '2 bedrooms','3 bedrooms' ])
	# for key, value in sorted(pricePerChange.iteritems(), reverse=True):
	# 	writer.writerow([key.strftime("%y/%m/%d"), '{:,.2f}%'.format(value[0]*100), '{:,.2f}%'.format(value[1]*100), '{:,.2f}%'.format(value[2]*100)])

	# use pandas dataframe type to write csv file
	#### change the data structure from dictionary to dataframe
	### the unit price
	date=np.array(pricePerUnit.items())[:,0]
	price=np.array(pricePerUnit.items())[:,1]
	#get the price for each type of property
	price2Array=np.array([np.array(x) for x in price])
	bedroom1=price2Array[:,0]
	bedroom2=price2Array[:,1]
	bedroom3=price2Array[:,2]

	pricePerUnitDf=pd.DataFrame({'date':date, '1 bed': bedroom1, '2 bed': bedroom2, '3 bed': bedroom3})
	pricePerUnitDf['Suburb']=[enquirySub]*len(pricePerUnitDf.index)

	### the price per square
	date=np.array(pricePerSqm.items())[:,0]
	price=np.array(pricePerSqm.items())[:,1]
	#get the price for each type of property
	price2Array=np.array([np.array(x) for x in price])
	bedroom1=price2Array[:,0]
	bedroom2=price2Array[:,1]
	bedroom3=price2Array[:,2]

	pricePerSqmDf=pd.DataFrame({'date':date, '1 bed': bedroom1, '2 bed': bedroom2, '3 bed': bedroom3})
	pricePerSqmDf['Suburb']=[enquirySub]*len(pricePerSqmDf.index)

	### the price of change
	date=np.array(pricePerChange.items())[:,0]
	price=np.array(pricePerChange.items())[:,1]
	#get the price for each type of property
	price2Array=np.array([np.array(x) for x in price])
	bedroom1=price2Array[:,0]
	bedroom2=price2Array[:,1]
	bedroom3=price2Array[:,2]

	pricePerChangeDf=pd.DataFrame({'date':date, '1 bed': bedroom1, '2 bed': bedroom2, '3 bed': bedroom3})
	#print enquirySub
	pricePerChangeDf['Suburb']=[enquirySub]*len(pricePerChangeDf.index)

	print pricePerUnitDf 
	print pricePerSqmDf
	print pricePerChangeDf
	#import pdb; pdb.set_trace()

	


	###import the result to database propertyPrice_database
	con=MySQLdb.connect("localhost", "root", "1111", "propertyPrice_database")
	cursor=con.cursor()
	
	pricePerUnitSql=pricePerUnitDf.copy()
	#import pdb; pdb.set_trace()
	pricePerUnitSql.rename(columns={'1 bedroom':'one_bedroom', '2 bedrooms':'two_bedrooms', '3 bedrooms':'three_bedrooms'}, inplace=True)
	pricePerUnitSql.to_sql(con=con, name='price_per_unit', if_exists='append', flavor='mysql', index=False)

	pricePerSqmSql=pricePerSqmDf.copy()
	#import pdb; pdb.set_trace()
	pricePerSqmSql.rename(columns={'1 bedroom':'one_bedroom', '2 bedrooms':'two_bedrooms', '3 bedrooms':'three_bedrooms'}, inplace=True)
	pricePerSqmSql.to_sql(con=con, name='price_per_sqm', if_exists='append', flavor='mysql', index=False)

	pricePerChangeSql=pricePerChangeDf.copy()
	#import pdb; pdb.set_trace()
	pricePerChangeSql.rename(columns={'1 bedroom':'one_bedroom', '2 bedrooms':'two_bedrooms', '3 bedrooms':'three_bedrooms'}, inplace=True)
	pricePerChangeSql.to_sql(con=con, name='rate_of_change', if_exists='append', flavor='mysql', index=False)
	con.close()




	# 

	# outputFile.close()


if __name__=='__main__':

	# startDate="2016-01-20"
	# enquirySub="EPPING"
	# interval=10
	#enquirySub="ASHFIELD"
	

	# parser=optparse.OptionParser()

	# parser.add_option("-a", "--statusAvailable", help="only consider the available properties",dest="statusCheck", action="store_true", default=False)

	# (options, args)=parser.parse_args(sys.argv)

	# enquirySub=sys.argv[1]
	# startDate=sys.argv[2]
	# interval=sys.argv[3]

	parserArg=argparse.ArgumentParser()
	

	parserArg.add_argument("enquirySub")
	parserArg.add_argument("startDate")
	parserArg.add_argument("interval", type=int)
	parserArg.add_argument("-a", "--statusAvailable", help="only consider the available properties",dest="statusCheck", action="store_true", default=False)


	args=parserArg.parse_args( )

	#import pdb; pdb.set_trace()
	result=intervalPrice(args.enquirySub, args.startDate, args.interval, args.statusCheck)
	priceDic2csv(result,args.enquirySub)







