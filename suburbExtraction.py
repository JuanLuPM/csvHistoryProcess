import csv
from re import sub
from decimal import Decimal
import numpy as np
import sys



""" extract the data of a certain suburb from the csv file and 
calculate the median price per unit and per square. The result is shown based on the number of bedrooms from 1 to 3. 
"""

def suburbExtraction(enquirySub, enquiryTable, statusCheck=None):

	#filteredRow=[]
	bedroom1=[]
	bedroom2=[]
	bedroom3=[]
	priceBedroom1=[]
	priceBedroom2=[]
	priceBedroom3=[]

	areaBedroom1=[]
	areaBedroom2=[]
	areaBedroom3=[]
	
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

						Bed1=["1","1+S"]
						Bed2=["2", "2+S"]
						Bed3=["3", "3+S"]	
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
								if len(currentPrice) <= 0:
									continue
								priceValue= Decimal(sub(r'[^\d.]', '', currentPrice))

								# priceValue= currentPrice[1:len(currentPrice)]
								# print ast.literal_eval(priceValue)
								priceBedroom1.append(float(priceValue))

								#calculate the area
								currentArea=row['Internal Area']
								if currentArea.endswith('m2'):
									currentArea=currentArea[0:-2]
								areaBedroom1.append(float(currentArea))

							if row['Bedrooms'] in  Bed2: 
								currentPrice=row['Price']
								if bool(currentPrice):
									#print currentPrice
									priceValue= Decimal(sub(r'[^\d.]', '', currentPrice))

									priceBedroom2.append(float(priceValue))

									#import pdb; pdb.set_trace()
									currentArea=row['Internal Area']
									if currentArea.endswith('m2'):
										currentArea=currentArea[0:-2]
									areaBedroom2.append(float(currentArea))


							if row['Bedrooms'] in  Bed3: 
								currentPrice=row['Price']
								if bool(currentPrice):
									priceValue= Decimal(sub(r'[^\d.]', '', currentPrice))
									priceBedroom3.append(float(priceValue))
									currentArea=row['Internal Area']
									if currentArea.endswith('m2'):
										currentArea=currentArea[0:-2]
									areaBedroom3.append(float(currentArea))
						else:
							continue
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

	# priceBedroom1=np.array(priceBedroom1)
	#print count
	if count!=0:
		if  priceBedroom1:
			medianBedroom1=np.median(priceBedroom1)
			#averageBedroom1=np.average(priceBedroom1)
			perSqm1=np.median(np.divide(priceBedroom1, areaBedroom1))
		else:
			medianBedroom1=0
			perSqm1=0
		

		if  priceBedroom2:
			medianBedroom2=np.median(priceBedroom2)
			#averageBedroom2=np.average(priceBedroom2)
			perSqm2=np.median(np.divide(priceBedroom2, areaBedroom2))
		else:
			medianBedroom2=0
			perSqm2=0

		#import pdb; pdb.set_trace()
		if  priceBedroom3:
			medianBedroom3=np.median(priceBedroom3)
			#averageBedroom3=np.average(priceBedroom3)
			perSqm3=np.median(np.divide(priceBedroom3, areaBedroom3))
		else:
			medianBedroom3=0
			perSqm3=0

		# print 'per unit'
		# print medianBedroom1
		# print medianBedroom2
		# print medianBedroom3

		# print '\nper sqm'
		# print perSqm1
		# print perSqm2
		# print perSqm3
		# print '\n'

		return {'price per unit':[medianBedroom1,medianBedroom2,medianBedroom3], 'price per sqm':[perSqm1,perSqm2,perSqm3]}
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




