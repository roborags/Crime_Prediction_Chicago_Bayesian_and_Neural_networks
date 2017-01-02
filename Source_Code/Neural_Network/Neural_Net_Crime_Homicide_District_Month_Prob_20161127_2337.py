import csv
import re
import math
import random

#........................................ Global variables.................................................#

Probabilty_Homicide_district_ = [0 for x in range(26)]
Probabilty_Homicide_Month_ = [0 for x in range(13)]
Probabilty_Arson_district_ = [0 for x in range(26)]
Probabilty_Arson_Month_ = [0 for x in range(13)]
Probabilty_CriminalDamage_district_ = [0 for x in range(26)]
Probabilty_CriminalDamage_Month_ = [0 for x in range(13)]
ReqProb_Dist_Month_Homicide = [[[0 for x in range(13)] for y in range(26)] for year in range(14)]
ReqProb_Dist_Month_Arson = [[[0 for x in range(13)] for y in range(26)] for year in range(14)]
ReqProb_Dist_Month_CriminalDamage = [[[0 for x in range(13)] for y in range(26)] for year in range(14)]


# while (Error >0.2):



#.................................. Probability distribution of Distrcit for homicide..................................#

	
def Probabilty_Homicide_district(District,Read_file):
	
	count=0
	sum1=0
	csv_f_reader=csv.reader(Read_file)
	for row in csv_f_reader:
		if row[5] == 'HOMICIDE':
			if row[11] != "true" and row[11] != "false" and row[11] != "TRUE" and row[11] != "FALSE" and row[11] !="" and int(row[11])<26:
				District[count] = int(row[11])											#conversion of string to int
				Probabilty_Homicide_district_[District[count]]=Probabilty_Homicide_district_[District[count]]+1
				#print(District[count])
				count=count+1
	for x in range (1,26):
		Probabilty_Homicide_district_[x]=Probabilty_Homicide_district_[x]/count
		sum1=sum1+Probabilty_Homicide_district_[x]
	print("The total prob of district is ",sum1)

#.................................. Probability distribution of Distrcit for Arson..................................#		

def Probabilty_Arson_district(District,Read_file):
	
	count=0
	sum1=0
	Read_file.seek(0)
	csv_f_reader=csv.reader(Read_file)
	for row in csv_f_reader:
		if row[5] == 'ARSON':
			if row[11] != "true" and row[11] != "false" and row[11] != "TRUE" and row[11] != "FALSE" and row[11] !="" and int(row[11])<26:
				# print(count)
				District[count] = int(row[11])											#conversion of string to int
				Probabilty_Arson_district_[District[count]]=Probabilty_Arson_district_[District[count]]+1
				count=count+1
	for x in range (1,26):
		Probabilty_Arson_district_[x]=Probabilty_Arson_district_[x]/count
		sum1=sum1+Probabilty_Arson_district_[x]
		print("The district value is ",Probabilty_Arson_district_[x])
	print("The total prob of district is ",sum1)
	
#.................................. Probability distribution of Distrcit for CriminalDamage..................................
	
def Probabilty_CriminalDamage_district(District,Read_file):
	
	count=0
	sum1=0
	Read_file.seek(0)
	csv_f_reader=csv.reader(Read_file)
	for row in csv_f_reader:
		if row[5] == 'CRIMINAL DAMAGE':
			if row[11] != "true" and row[11] != "false" and row[11] != "TRUE" and row[11] != "FALSE" and row[11] !="" and int(row[11])<26:
				# print(row," the count is",count)
				District[count] = int(row[11])											#conversion of string to int
				Probabilty_CriminalDamage_district_[District[count]]=Probabilty_CriminalDamage_district_[District[count]]+1
				count=count+1

	for x in range (1,26):
		Probabilty_CriminalDamage_district_[x]=Probabilty_CriminalDamage_district_[x]/count
		sum1=sum1+Probabilty_CriminalDamage_district_[x]
	print("The total prob of district is ",sum1)
	
	
#.................................. Probability distribution of month for homicide..................................#

def Probabilty_Homicide_Month(Month_homicide,District_month_homicide):

	count=0
	sum1=0
	for count in range(0,len(Month_homicide)):
		District_month_homicide[count] = Month_homicide[count]											
		Probabilty_Homicide_Month_[District_month_homicide[count]]=Probabilty_Homicide_Month_[District_month_homicide[count]]+1
		# print("The value of monthh is ",District_month_homicide[count])
		count=count+1
	for x in range (1,13):
		# print(Probabilty_Homicide_Month_[x])
		Probabilty_Homicide_Month_[x]=Probabilty_Homicide_Month_[x]/(count-1)
		sum1=sum1+Probabilty_Homicide_Month_[x]
		# print("The total prob of month is ",sum1)

	
#.................................. Probability distribution of month for Arson..................................#

def Probabilty_Arson_Month(Month_Arson,District_month_arson):

	count=0
	sum1=0

	for count in range(0,len(Month_Arson)):
		District_month_arson[count] = Month_Arson[count]											
		Probabilty_Arson_Month_[District_month_arson[count]]=Probabilty_Arson_Month_[District_month_arson[count]]+1
		count=count+1

	for x in range (1,13):
		# print(Probabilty_Arson_Month_[x])
		Probabilty_Arson_Month_[x]=Probabilty_Arson_Month_[x]/(count-1)
		sum1=sum1+Probabilty_Arson_Month_[x]
		# print("The total prob of month is ",sum1)
	
#.................................. Probability distribution of month for CriminalDamage..................................#

def Probabilty_CriminalDamage_Month(Month_CriminalDamage,District_month_CriminalDamage):

	count=0
	sum1=0

	for count in range(0,len(Month_CriminalDamage)):
		District_month_CriminalDamage[count] = Month_CriminalDamage[count]											
		Probabilty_CriminalDamage_Month_[District_month_CriminalDamage[count]]=Probabilty_CriminalDamage_Month_[District_month_CriminalDamage[count]]+1
		count=count+1
		
	for x in range (1,13):
		# print(Probabilty_CriminalDamage_Month_[x])
		Probabilty_CriminalDamage_Month_[x]=Probabilty_CriminalDamage_Month_[x]/(count-1)
		sum1=sum1+Probabilty_CriminalDamage_Month_[x]
		# print("The total prob of month is ",sum1)
	

#............................Month calculation..................................#

def Month(row,count_date):
	date_int=0
	if re.search(r'[/]',row[2]):
		date=row[2].split("/")
		print("The date is ",date[0])
	elif re.search(r'[-]',row[2]):
		date=row[2].split("-")
		# print("The date is ",date[0])
	date_int = int (date[0])
	# print("The month is ",date_int)
	return date_int

#....................................The main function....................................#

def main():

	w1=[random.randint(1,25) for district in range (1,26)]
	w2=[random.randint(1,13) for month in range (1,13)]
	w3=[random.randint(1,13) for year in range (1,13)]
	count_test1=[0 for x in range (1,14)]
	w_out1=random.randint(0,10)
	w_out2=random.randint(0,10)
	w_out3=random.randint(0,10)
	b1=0
	bout_1=0


	learningrate=100
	TotalCrimeCount = [0 for x in range(1,16)]
#....................................................	Split the crimes based on Primary types....................................................#
	for year in range (1,14):
		if year == 1:
			f=open("Trainingdata_2001.csv")
			Read_file=open("Trainingdata_2001.csv")
			Read_Date=open("Trainingdata_2001.csv")
			csv_f=csv.reader(f)
		elif year == 2:
			f=open("Trainingdata_2002.csv")
			Read_file=open("Trainingdata_2002.csv")
			Read_Date=open("Trainingdata_2002.csv")
			csv_f=csv.reader(f)
		elif year ==3:
			f=open("Trainingdata_2003.csv")
			Read_file=open("Trainingdata_2003.csv")
			Read_Date=open("Trainingdata_2003.csv")
			csv_f=csv.reader(f)
		elif year ==4:
			f=open("Trainingdata_2004.csv")
			Read_file=open("Trainingdata_2004.csv")
			Read_Date=open("Trainingdata_2004.csv")
			csv_f=csv.reader(f)
		elif year ==5:
			f=open("Trainingdata_2005.csv")
			Read_file=open("Trainingdata_2005.csv")
			Read_Date=open("Trainingdata_2005.csv")
			csv_f=csv.reader(f)
		elif year == 6:
			f=open("Trainingdata_2006.csv")
			Read_file=open("Trainingdata_2006.csv")
			Read_Date=open("Trainingdata_2006.csv")
			csv_f=csv.reader(f)
		elif year ==7:
			f=open("Trainingdata_2007.csv")
			Read_file=open("Trainingdata_2007.csv")
			Read_Date=open("Trainingdata_2007.csv")
			csv_f=csv.reader(f)
		elif year == 8:
			f=open("Trainingdata_2008.csv")
			Read_file=open("Trainingdata_2008.csv")
			Read_Date=open("Trainingdata_2008.csv")
			csv_f=csv.reader(f)
		elif year ==9:
			f=open("Trainingdata_2009.csv")
			Read_file=open("Trainingdata_2009.csv")
			Read_Date=open("Trainingdata_2009.csv")
			csv_f=csv.reader(f)
		elif year ==10:
			f=open("Trainingdata_2010.csv")
			Read_file=open("Trainingdata_2010.csv")
			Read_Date=open("Trainingdata_2010.csv")
			csv_f=csv.reader(f)
		elif year ==11:
			f=open("Trainingdata_2011.csv")
			Read_file=open("Trainingdata_2011.csv")
			Read_Date=open("Trainingdata_2011.csv")
			csv_f=csv.reader(f)
		elif year ==12:
			f=open("Trainingdata_2012.csv")
			Read_file=open("Trainingdata_2012.csv")
			Read_Date=open("Trainingdata_2012.csv")
			csv_f=csv.reader(f)
		elif year ==13:
			f=open("Testing_Data_2013.csv")
			Read_file=open("Testing_Data_2013.csv")
			Read_Date=open("Testing_Data_2013.csv")
			csv_f=csv.reader(f)
		count_homicide=1
		count_arson=1
		count_criminal_damage=1
		count=0
		for row in csv_f:
			count=count+1
			# print(row[5])
			if row[5] == 'ARSON':
				count_arson=count_arson+1
			elif row[5] == 'HOMICIDE':
				count_homicide=count_homicide+1
			if row[5] == 'CRIMINAL DAMAGE':
				count_criminal_damage=count_criminal_damage+1
		
		TotalCrimeCount[year]= count

#.........................................................................................#
#.........................................................................................#
#.........................................................................................#
#.........................Finding the probabilty of Homicide..............................#
#.........................................................................................#
#.........................................................................................#
#.........................................................................................#
		# print("Homicide count for the ",year," training year is ",count_homicide)
		
#................................... District Probability Distribution for Homicide..................................#

		District_homicide = [0 for x in range(count_homicide)]
		Probabilty_Homicide_district(District_homicide,Read_file)
		f.close()
		# for x in range(1,26):
			# print("The probabilty of homicide district ",x," is: ",Probabilty_Homicide_district_[x])

#................................... Month Probability Distribution for Homicide..................................#

		date_int = 0
		Month_homicide=[0 for x in range (count_homicide)]
		District_month_homicide = [0 for x in range(count_homicide)]
		
		count_date_=0
		sum1=0
		
		csv_f_reader_month=csv.reader(Read_Date)
		# print(row)
		# row=0
		for row in csv_f_reader_month:
			
			if row[5] == 'HOMICIDE':
				
				Month_homicide[count_date_]=Month(row,count_date_)
				# print("The month is ",Month_homicide[count_date_])
				count_date_=count_date_+1
		# print("count for homicide date is",count_date_)
		
		Probabilty_Homicide_Month(Month_homicide,District_month_homicide)
		# for x in range(1,13):
			# print(Probabilty_Homicide_Month_[x])
		for x in range (1,26):
			for y in range (1,13):
				ReqProb_Dist_Month_Homicide[year][x][y] = Probabilty_Homicide_Month_[y]*Probabilty_Homicide_district_[x]
				# print("The probability year",year,"District is",x,"month is ",y," of homicide is ",ReqProb_Dist_Month_Homicide[year][x][y])
				sum1=sum1+ReqProb_Dist_Month_Homicide[year][x][y]
		print(sum1)

#.........................................................................................#
#.........................................................................................#
#.........................................................................................#
#.................Adding Weights for getting 2013 data (Linear regression)................#
#.........................................................................................#
#.........................................................................................#
#.........................................................................................#

	Prob_CriminalDamage_2013 = [[0 for x in range(13)] for y in range(26)]
	Prob_Arson_2013 = [[0 for x in range(13)] for y in range(26)]
	Prob_Homicide_2013 = [[0 for x in range(13)] for y in range(26)]
	test_homicide_prob = [[[0 for x in range(13)] for y in range(26)] for year in range(14)]
	sum1=0
	Error =1.0
	for district in range(1,26):
		for month in range (1,13):
			sum1=0
			for year in range (1,13):
				# Prob_CriminalDamage_2013[x][y] = Prob_CriminalDamage_2013[x][y] + year * ReqProb_Dist_Month_CriminalDamage[year][x][y]
				# Prob_Arson_2013[x][y] = Prob_Arson_2013[x][y] + year * ReqProb_Dist_Month_Arson[year][x][y]
				Prob_Homicide_2013[district][month] = Prob_Homicide_2013[x][month] + year * ReqProb_Dist_Month_Homicide[year][district][month]
				sum1=sum1+year
			Prob_Homicide_2013[district][month] = Prob_Homicide_2013[district][month]/sum1

	error=1.0
	delta_1=0.0
	delta_2=0.0
	district_ = [x for x in range(1,27)]
	month_= [x for x in range (1,14)]
	year_ = [x for x in range (1,14)]
	for test in range(0,50):
		# HiddenLayer()
		for district in range (1,2):
			if district != 13 and district != 21 and district !=23:
				for month in range (1,13):
					for year in range(1,13):
						for chumma in range(1,2):
							neth1=w1[1]*district_[district]/325 + w2[1]*month_[month]/78 + w3[1]*(year_[year])/78 
							neth2=w1[2]*district_[district]/325 + w2[2]*month_[month]/78 + w3[2]*(year_[year])/78
							neth3=w1[3]*district_[district]/325 + w2[3]*month_[month]/78 + w3[3]*(year_[year])/78
							# print(neth1)
							outh1=(1/(1+math.pow(2.718,-neth1)))
							outh2=(1/(1+math.pow(2.718,-neth2)))
							outh3=(1/(1+math.pow(2.718,-neth3)))
								
							neto1= (w_out1*outh1) + (w_out2*outh2) + (w_out3*outh3) + (bout_1*1)
								
							outo1=(1/(1+math.pow(2.718,-neto1)))
								
							# error=0.5* math.pow((neto1-Prob_Homicide_2013[district][month]),2)
								
							delta_1=(outo1-ReqProb_Dist_Month_Homicide[year][district][month])*outo1*(1-outo1)
								
							w_out1=w_out1-learningrate*delta_1
							w_out2=w_out2-learningrate*delta_1
							w_out3=w_out3-learningrate*delta_1
								
							w1[1]=w1[1]-learningrate*(delta_1*outh1 + delta_1*outh2 + delta_1*outh3 )*(1-outh1)*district_[district]*w1[1]
							w2[1]=w2[1]-learningrate*(delta_1*outh1 + delta_1*outh2 + delta_1*outh3 )*(1-outh1)*month_[month]*w2[1]
							w3[1]=w3[1]-learningrate*(delta_1*outh1 + delta_1*outh2 + delta_1*outh3 )*(1-outh2)*year_[year]*w3[1]
							w1[2]=w1[2]-learningrate*(delta_1*outh1 + delta_1*outh2 + delta_1*outh3 )*(1-outh1)*district_[district]*w1[2]
							w2[2]=w2[2]-learningrate*(delta_1*outh1 + delta_1*outh2 + delta_1*outh3 )*(1-outh1)*month_[month]*w2[2]
							w3[2]=w3[2]-learningrate*(delta_1*outh1 + delta_1*outh2 + delta_1*outh3 )*(1-outh2)*year_[year]*w3[2]
							w1[3]=w1[3]-learningrate*(delta_1*outh1 + delta_1*outh2 + delta_1*outh3 )*(1-outh1)*district_[district]*w1[3]
							w2[3]=w2[3]-learningrate*(delta_1*outh1 + delta_1*outh2 + delta_1*outh3 )*(1-outh1)*month_[month]*w2[3]
							w3[3]=w3[3]-learningrate*(delta_1*outh1 + delta_1*outh2 + delta_1*outh3 )*(1-outh2)*year_[year]*w3[3]
							
	print("outo1 of 2013 is")
	for  district in range (1,26):
		for month in range(1,13):
			neth1=w1[1]*district_[district]/325 + w2[1]*month_[month]/78 + w3[1]*13/91 
			neth2=w1[2]*district_[district]/325 + w2[2]*month_[month]/78 + w3[2]*13/91
			neth2=w1[3]*district_[district]/325 + w2[3]*month_[month]/78 + w3[3]*13/91			
			outh1=(1/(1+math.pow(2.718,-neth1)))
			outh2=(1/(1+math.pow(2.718,-neth2)))
			outh3=(1/(1+math.pow(2.718,-neth3)))			
			neto1= (w_out1*outh1) + (w_out2*outh2) + (w_out3*outh3) + (bout_1*1)
			
			outo1=(1/(1+math.pow(2.718,-neto1)))
			print(outo1)
			
			

#................................. Main function call .................................#	

main()