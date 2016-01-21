import csv
from re import sub
from decimal import Decimal
import numpy as np
import sys



# roject_id,ID,Lot Name,Unit No,Price,Bedrooms,Level,Bathrooms,Parkings,Internal Area,
# External Area,Aspect,Storage,Sale Status,Floor Plan,Comment,Created At,Project,Price_from_developer,Sale_Status_from_developer,
# Land Size,Land Length,Land Width,Clicked

# INTERNALAREACOL=9
# BEDROOMCOL=5
# SUBURBCOL=17
# PRICECOL=4
# DATECOL=16

def suburbExtraction(enquirySub, enquiryTable):

	filteredRow=[]
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
	with open(enquiryTable, 'rb') as csvfile:
		#reader=csv.reader(csvfile)
		reader=csv.DictReader(csvfile)
		next(reader, None)
		for row in reader:
			# if count==0:	#the header of the table
			# 	print row[0]
			# 	newRow=[row[SUBURBCOL],row[INTERNALAREACOL], row[BEDROOMCOL], row[PRICECOL], row[DATECOL]]
			# 	filteredRow.append(newRow)
			# 	count=count+1
			projectName=row['Project']
			destinateStr=enquirySub
			po=projectName.find(destinateStr)
			
			if po>=0:
				#newRow=[row[SUBURBCOL],row[INTERNALAREACOL], row[BEDROOMCOL], row[PRICECOL], row[DATECOL]]
				#filteredRow.append(newRow)

				Bed1=["1","1+S"]
				Bed2=["2", "2+S"]
				Bed3=["3", "3+S"]	

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
					areaBedroom1.append(float(currentArea))

				if row['Bedrooms'] in  Bed2: 
					currentPrice=row['Price']
					if bool(currentPrice):
						#print currentPrice
						priceValue= Decimal(sub(r'[^\d.]', '', currentPrice))

						priceBedroom2.append(float(priceValue))

						currentArea=row['Internal Area']
						areaBedroom2.append(float(currentArea))


				if row['Bedrooms'] in  Bed3: 
					currentPrice=row['Price']
					if bool(currentPrice):
						priceValue= Decimal(sub(r'[^\d.]', '', currentPrice))
						priceBedroom3.append(float(priceValue))
						currentArea=row['Internal Area']
						areaBedroom3.append(float(currentArea))

	# priceBedroom1=np.array(priceBedroom1)
	medianBedroom1=np.median(priceBedroom1)
	averageBedroom1=np.average(priceBedroom1)
	perSqm1=np.median(np.divide(priceBedroom1, areaBedroom1))

	medianBedroom2=np.median(priceBedroom2)
	averageBedroom2=np.average(priceBedroom2)
	perSqm2=np.median(np.divide(priceBedroom2, areaBedroom2))

	medianBedroom3=np.median(priceBedroom3)
	averageBedroom3=np.average(priceBedroom3)
	perSqm3=np.median(np.divide(priceBedroom3, areaBedroom3))

	print 'per unit'
	print medianBedroom1
	print medianBedroom2
	print medianBedroom3

	print '\nper sqm'
	print perSqm1
	print perSqm2
	print perSqm3


if __name__=='__main__':

	#enquirySub="ASHFIELD"
	enquirySub=sys.argv[1]
	enquiryTable=sys.argv[2]
	print enquiryTable+'\n'  ###'../suburb_profiling/history_data/2016_01_20_lots.csv'
	suburbExtraction(enquirySub, enquiryTable)

		# count=count+1

		# if count==204: 
		# 	print row[16]
		# 	break
		# else:
		# 	continue 
		# if a==0:
		# 	break

#print filteredRow

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




