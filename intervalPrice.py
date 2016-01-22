"""
search the *.csv files to get the price result in a certain period. 
"""

import dateutil.parser as dparser
import datetime
import csv 
from suburbExtraction import * 
import os.path
import sys


fileDir='/Users/juanlu/Workspace/suburb_profiling/history_data/'

def intervalPrice(enquirySub, startDate, interval):
	##extract the year, month and date
	startPoint=dparser.parse(startDate,fuzzy=True)

	#endPoint=startPoint-datetime.timedelta(days=20)

	#get the date list
	#print startPoint
	daysList=[startPoint-datetime.timedelta(days=x) for x in range(0, interval)]
	#print dateList

	priceUnitDic={}
	priceSqmDic={}
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
			currentPrice=suburbExtraction(enquirySub, fileFullPath)
			if currentPrice!=None:
				#print currentPrice
				priceUnitDic[days]=currentPrice['price per unit']
				priceSqmDic[days]=currentPrice['price per sqm']
				#print priceUnitDic,priceSqmDic
	return [priceUnitDic, priceSqmDic]			

    # if (os.path.isfile(fileFullPath)==Ture):
    # 	print currentDate
		#suburbExtraction(enquirySub, fileFullPath)

	# print fileFullPath

	# f=open(fileFullPath, 'rb')

	# print f
	# f.close()
	#break
def priceDic2csv(priceDic):
  	 pricePerUnit=priceDic[0]
  	 pricePerSqm=priceDic[1]

  	 #print pricePerUnit
  	 #print pricePerSqm 

  	 outputFile=open('result.csv', 'w')
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

  	 outputFile.close()


if __name__=='__main__':

	# startDate="2016-01-20"
	# enquirySub="EPPING"
	# interval=10
	#enquirySub="ASHFIELD"
	enquirySub=sys.argv[1]
	startDate=sys.argv[2]
	interval=sys.argv[3]

	result=intervalPrice(enquirySub, startDate, int(interval))
	priceDic2csv(result)