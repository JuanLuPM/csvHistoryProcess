""" extract the data of a certain suburb from the csv file and 
calculate the statistical results of price per unit and per square. 
"""

import csv
from re import sub 
import numpy as np 
import pandas as pd 
from decimal import Decimal 
import sys
import argparse


def suburbExtraction(enquirySub, enquiryTable, statusCheck=None):
	fields=['Project', 'Bedrooms', 'Internal Area', 'Price', 'Sale Status']

	df=pd.read_csv(enquiryTable,  usecols=fields)

	# print df.values
	# import pdb; pdb.set_trace()

	## check if it is a blank table 
	if np.all(df.values, None)==True:
		return None

	dfWithEnquirySub=df[df['Project'].str.contains(enquirySub)==True]
	dfProcess=dfWithEnquirySub
	#import pdb; pdb.set_trace()
	#print dfWithEnquirySub

	#check the status
	if statusCheck=='a':
		dfWithAvailable=dfWithEnquirySub[dfWithEnquirySub['Sale Status'].str.contains('Available')==True]
		dfProcess=dfWithAvailable
		#print dfWithAvailable

	#import pdb; pdb.set_trace()
	#get one bedroom data
	dfBedrooms1=dfProcess[dfProcess['Bedrooms'].str.contains("1|1+S")==True]	
	
	priceValue=dfBedrooms1['Price'].values
	priceValue=[Decimal(sub(r'[^\d.]', '', x) ) for x in priceValue]
	priceValue=[float(x) for x in priceValue]
	priceBedrooms1=priceValue

	#print priceBedrooms1

	areaBedrooms1=dfBedrooms1['Internal Area']
	#print priceBedrooms1, areaBedrooms1

	# get data of two bedrooms
	dfBedrooms2=dfProcess[dfProcess['Bedrooms'].str.contains("2|2+S")==True]	
	
	priceValue=dfBedrooms2['Price'].values
	priceValue=[float(Decimal(sub(r'[^\d.]', '', x) )) for x in priceValue]
	priceBedrooms2=priceValue
	areaBedrooms2=dfBedrooms2['Internal Area']

	# get data of three bedrooms
	dfBedrooms3=dfProcess[dfProcess['Bedrooms'].str.contains("3|3+S")==True]	
	
	priceValue=dfBedrooms3['Price'].values
	priceValue=[float(Decimal(sub(r'[^\d.]', '', x) )) for x in priceValue]
	priceBedrooms3=priceValue
	areaBedrooms3=dfBedrooms3['Internal Area']

	
	medianBedroom1=np.median(priceBedrooms1)
	#averageBedroom1=np.average(priceBedroom1)
	
	avePrice=np.divide(priceBedrooms1, areaBedrooms1.values.astype('float64'))
	perSqm1=np.median(avePrice)
	#perSqm1=np.median(np.divide(priceBedrooms1, areaBedrooms1.values.astype('float64')))
	

	medianBedroom2=np.median(priceBedrooms2)
	#averageBedroom2=np.average(priceBedroom2)
	perSqm2=np.median(np.divide(priceBedrooms2, areaBedrooms2.values.astype('float64')))

	#import pdb; pdb.set_trace()
	medianBedroom3=np.median(priceBedrooms3)
	#averageBedroom3=np.average(priceBedroom3)
	avePrice=np.divide(priceBedrooms3, areaBedrooms3.values.astype('float64'))
	perSqm3=np.median(avePrice)
	#perSqm3=np.median(np.divide(priceBedrooms3, areaBedrooms3.values.astype('float64')))

	# print 'per unit'
	# print medianBedroom1
	# print medianBedroom2
	# print medianBedroom3

	# print '\nper sqm'
	# print perSqm1
	# print perSqm2
	# print perSqm3
	# print '\n'

	result={'price per unit':[medianBedroom1,medianBedroom2,medianBedroom3], 
			'price per sqm':[perSqm1,perSqm2,perSqm3]}

	resultDf=pd.DataFrame(result, columns=result.keys())

	print resultDf 
	#import pdb; pdb.set_trace()
	

if __name__=='__main__':

	parser=argparse.ArgumentParser()

	parser.add_argument("enquirySub")
	parser.add_argument("enquiryTable")
	parser.add_argument("enquiryStatus")

	args=parser.parse_args()

	suburbExtraction(args.enquirySub, args.enquiryTable, args.enquiryStatus)

