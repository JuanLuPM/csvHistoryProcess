"""
search the *.csv files to get the price result in a certain period. 
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


fileDir='/Users/juanlu/Workspace/suburb_profiling/history_data/'

def intervalPrice(enquirySub, startDate, interval, statusCheck):
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

	priceChangeDic[dayAfter]=[0,0,0]
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
def priceDic2csv(priceDic):
	"""put the data in priceDic to result.csv 
	"""
  	pricePerUnit=priceDic[0]
  	pricePerSqm=priceDic[1]
  	pricePerChange=priceDic[2]

  	 #print pricePerUnit
  	 #print pricePerSqm 

  	outputFile=open('output.csv', 'w')
  	writer=csv.writer(outputFile)
	writer.writerow(["price per unit"])
	writer.writerow([ None,'1 bedroom', '2 bedrooms','3 bedrooms' ])
	for key, value in sorted(pricePerUnit.iteritems(), reverse=True):
		writer.writerow([key.strftime("%y/%m/%d"), '${:,.2f}'.format(value[0]), '${:,.2f}'.format(value[1]), '${:,.2f}'.format(value[2])])

	writer.writerow([])	
	writer.writerow(["price per sqm"])
	writer.writerow([ None,'1 bedroom', '2 bedrooms','3 bedrooms' ])
	for key, value in sorted(pricePerSqm.iteritems(), reverse=True):
		writer.writerow([key.strftime("%y/%m/%d"), '${:,.2f}'.format(value[0]), '${:,.2f}'.format(value[1]), '${:,.2f}'.format(value[2])])

	writer.writerow([])
	writer.writerow(["rate of change"])
	writer.writerow([ None,'1 bedroom', '2 bedrooms','3 bedrooms' ])
	for key, value in sorted(pricePerChange.iteritems(), reverse=True):
		writer.writerow([key.strftime("%y/%m/%d"), '{:,.2f}%'.format(value[0]*100), '{:,.2f}%'.format(value[1]*100), '{:,.2f}%'.format(value[2]*100)])



	outputFile.close()


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
	priceDic2csv(result)







