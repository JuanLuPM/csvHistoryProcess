import csv
from re import sub
from decimal import Decimal
import numpy as np
import sys
import pandas as pd


""" extract the data of a certain suburb from the csv file and 
calculate the median price per unit and per square. The result is shown based on the number of bedrooms from 1 to 3. 
"""

def suburbExtraction(enquirySub, enquiryTable, statusCheck=None):

	#filteredRow=[]
	bedroom1=[]
	bedroom2=[]
	bedroom3=[]
	bedroom4=[]
	studio=[]

	priceBedroom1=[]
	priceBedroom2=[]
	priceBedroom3=[]
	priceBedroom4=[]
	priceStudio=[]

	areaBedroom1=[]
	areaBedroom2=[]
	areaBedroom3=[]
	areaBedroom4=[]
	areaStudio=[]
	
	count=0
	#import pdb; pdb.set_trace()
	# if statusCheck=='a':
	# 	check=1     #only check the available property
	# else
	# 	check=0

	with open(enquiryTable, 'rb') as csvfile:
		#reader=csv.reader(csvfile)
		reader=csv.DictReader(csvfile)
		next(reader, None)
		try: 
			for row in reader:
				# if count==0:	#the header of the table
				# 	print row[0]
				# 	newRow=[row[SUBURBCOL],row[INTERNALAREACOL], row[BEDROOMCOL], row[PRICECOL], row[DATECOL]]
				# 	filteredRow.append(newRow)
				# 	count=count+1
				if row!=None:
					
					projectName=row['Project']
					destinateStr=enquirySub
					po=projectName.find(destinateStr)
					

					if po>=0:
						#newRow=[row[SUBURBCOL],row[INTERNALAREACOL], row[BEDROOMCOL], row[PRICECOL], row[DATECOL]]
						#filteredRow.append(newRow)

						Bed1=["1", "1+S", "1+M", "1 Bed", "1 Bed+S", "1 Bed+M"]
						Bed2=["2", "2+S", "2+M", "2 Bed", "2 Bed+S", "2 Bed+M"]
						Bed3=["3", "3+S", "3+M", "3 Bed", "3 Bed+S", "3 Bed+M"]
						Bed4=["4", "4+S", "4+M", "4 Bed", "4 Bed+S", "4 Bed+M"]
						Studio=["Studio"]	
						currentStatus=row['Sale Status']
						#print currentStatus, statusCheck

						### check if the data should be added to the list 
						if (statusCheck=='a' and currentStatus=='Available'):  ##when the required status is availbe
							check=1
						elif statusCheck== None:  ##when there is no requirement on the status of properties
							check=1
						else:
							check=0

						#import pdb; pdb.set_trace()
						#print check

						if check==1:
							count=count+1
							#print count
							if row['Bedrooms'] in  Bed1: 
								currentPrice=row['Price']
								if bool(currentPrice):
									
									priceValue= Decimal(sub(r'[^\d.]', '', currentPrice))

								# priceValue= currentPrice[1:len(currentPrice)]
								# print ast.literal_eval(priceValue)
									priceBedroom1.append(float(priceValue))
								else:
									priceBedroom1.append(None)

								#calculate the area
								currentArea=row['Internal Area']
								if currentArea.endswith('m2'):
									currentArea=currentArea[0:-2]
								if currentArea:
									areaBedroom1.append(float(currentArea))
								else:
									areaBedroom1.append(None)

							if row['Bedrooms'] in  Bed2: 
								currentPrice=row['Price']
								if bool(currentPrice):
									#print currentPrice
									priceValue= Decimal(sub(r'[^\d.]', '', currentPrice))

									priceBedroom2.append(float(priceValue))
								else:
									priceBedroom2.append(None)

									#import pdb; pdb.set_trace()
								currentArea=row['Internal Area']
								if currentArea.endswith('m2'):
									currentArea=currentArea[0:-2]
								if currentArea:
									areaBedroom2.append(float(currentArea))
								else:
									areaBedroom2.append(None)


							if row['Bedrooms'] in  Bed3: 
								currentPrice=row['Price']
								if bool(currentPrice):
									priceValue= Decimal(sub(r'[^\d.]', '', currentPrice))
									priceBedroom3.append(float(priceValue))
								else:
									priceBedroom3.append(None)

								currentArea=row['Internal Area']
								if currentArea.endswith('m2'):
									currentArea=currentArea[0:-2]
								if currentArea:
									areaBedroom3.append(float(currentArea))
								else:
									areaBedroom3.append(None)


							if row['Bedrooms'] in  Bed4: 
								#import pdb; pdb.set_trace()
								currentPrice=row['Price']
								if bool(currentPrice):
									priceValue= Decimal(sub(r'[^\d.]', '', currentPrice))
									priceBedroom4.append(float(priceValue))
								else:
									priceBedroom4.append(None)

								currentArea=row['Internal Area']
								if currentArea.endswith('m2'):
									currentArea=currentArea[0:-2]
								if currentArea:
									areaBedroom4.append(float(currentArea))
								else:
									areaBedroom4.append(None)


							if row['Bedrooms'] in  Studio: 
								currentPrice=row['Price']
								if bool(currentPrice):
									priceValue= Decimal(sub(r'[^\d.]', '', currentPrice))
									priceStudio.append(float(priceValue))
								else:
									priceStudio.append(None)

								currentArea=row['Internal Area']
								if currentArea.endswith('m2'):
									currentArea=currentArea[0:-2]
								if currentArea:
									areaStudio.append(float(currentArea))
								else:
									areaStudio.append(None)
						else:
							continue
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

	# priceBedroom1=np.array(priceBedroom1)
	#import pdb; pdb.set_trace()
	#print count

	if count!=0:
		if  any(priceBedroom1): 
			# medianBedroom1=np.median(priceBedroom1)
			# #averageBedroom1=np.average(priceBedroom1)
			# if areaBedroom1:
			# 	perSqm1=np.median(np.divide(priceBedroom1, areaBedroom1))
			# else:
			# 	perSqm1=0
			df=pd.DataFrame({'price':priceBedroom1, 'area': areaBedroom1})
			medianBedroom1=df.median(axis=0)['price']

			if any(areaBedroom1):
				perSqmArray=df.price/df.area
				perSqm1=perSqmArray.median(axis=0)
			else:
				perSqm1=0

		else:
			medianBedroom1=0
			perSqm1=0
		

		if  any(priceBedroom2):
			
			df=pd.DataFrame({'price':priceBedroom2, 'area': areaBedroom2})
			medianBedroom2=df.median(axis=0)['price']

			if any(areaBedroom2):
				perSqmArray=df.price/df.area
				perSqm2=perSqmArray.median(axis=0)
			else:
				perSqm2=0
		else:
			medianBedroom2=0
			perSqm2=0

		#import pdb; pdb.set_trace()
		if  any(priceBedroom3):

			df=pd.DataFrame({'price':priceBedroom3, 'area': areaBedroom3})
			medianBedroom3=df.median(axis=0)['price']

			if any(areaBedroom3):
				perSqmArray=df.price/df.area
				perSqm3=perSqmArray.median(axis=0)
			else:
				perSqm3=0
		else:
			medianBedroom3=0
			perSqm3=0

		#import pdb; pdb.set_trace()
		if  any(priceBedroom4):
			df=pd.DataFrame({'price':priceBedroom4, 'area': areaBedroom4})
			medianBedroom4=df.median(axis=0)['price']

			if any(areaBedroom4):
				perSqmArray=df.price/df.area
				perSqm4=perSqmArray.median(axis=0)
			else:
				perSqm4=0
		else:
			medianBedroom4=0
			perSqm4=0

		if  any(priceStudio):

			df=pd.DataFrame({'price':priceStudio, 'area': areaStudio})
			medianStudio=df.median(axis=0)['price']

			if any(areaStudio):
				perSqmArray=df.price/df.area
				perSqmS=perSqmArray.median(axis=0)
			else:
				perSqmS=0

		else:
			medianStudio=0
			perSqmS=0


		# print 'per unit'
		# print medianBedroom1
		# print medianBedroom2
		# print medianBedroom3

		# print '\nper sqm'
		# print perSqm1
		# print perSqm2
		# print perSqm3
		# print '\n'
		#import pdb; pdb.set_trace()
		return {'price per unit':[medianBedroom1,medianBedroom2,medianBedroom3, medianBedroom4, medianStudio], 
				'price per sqm':[perSqm1,perSqm2,perSqm3, perSqm4, perSqmS]}

	else:
		#print "no data\n"
		return None






if __name__=='__main__':

	#enquirySub="ASHFIELD"
	enquirySub=sys.argv[1]
	enquiryTable=sys.argv[2]
	statusCheck=sys.argv[3]
	print enquiryTable+'\n'  ###'../suburb_profiling/history_data/2016_01_20_lots.csv'
	suburbExtraction(enquirySub, enquiryTable, statusCheck)

		# count=count+1

		# if count==204: 
		# 	print row[16]
		# 	break
		# else:
		# 	continue 
		# if a==0:
		# 	break



##get the average and medium price of the 1 bedrooms with or without studio


# filteredRow=["1 Bed", medianBedroom1, averageBedroom1]

# ########################
# #save the result as a csv file
# newFileName=enquirySub+".csv"
# #print newFileName
# resultFile=open(newFileName,'wb')
# writer=csv.writer(resultFile)
# writer.writerows(filteredRow)
# resultFile.close()




