import csv
import re
import math
import string

#........................................ Global variables.................................................#

Probabilty_Homicide_district_ = [0 for x in range(26)]
Probabilty_Homicide_Month_ = [0 for x in range(13)]
#Crime_Count_Year = [0 for x in range(13)]
#Crime_Count_Month = [0 for y in range(13)] 
#Crime_Count_District = [0 for z in range(26)]
Homicide_Count_Month = [0 for x in range(13)]
Homicide_Month_Prob = [0 for x in range(13)]
Crime_MD_Count = [[0 for y in range(13)] for x in range(26)]
Crime_Year_Count = [[[0 for z in range(16)] for y in range(13)] for x in range(26)]
#Crime_Count = [[0 for x in range(26)] for y in range(13)]
Crime_MD_Norm = [[0 for y in range(13)] for x in range(26)]
Crime_MD_Prob = [[0 for y in range(13)] for x in range(26)]
Homicide_Final_Prob = [[0 for y in range(13)] for x in range(26)]
Crime_Class_Count = [0 for x in range(11)]
Crime_Class_Prob = [0 for x in range(11)]
Crime_Class_Pred = [[[0 for z in range(11)] for y in range(13)] for x in range(26)]
Crime_District_Cond_Prob = [[0 for y in range(11)] for x in range(26)]
Crime_Month_Cond_Prob = [[0 for y in range(11)] for x in range(13)]
Crime_Final_Prob = [[[0 for z in range(11)] for y in range(13)] for x in range(26)]
Crime_Final_Class = [[0 for y in range(13)] for x in range(26)]
Crime_Final_Pred = [[0 for y in range(13)] for x in range(26)]

Crime_MD_Min = [[0 for y in range(13)] for x in range(26)]
Crime_MD_Max = [[0 for y in range(13)] for x in range(26)]
Crime_MD_Indv_Mean = [[0 for y in range(13)] for x in range(26)] 
Crime_MD_Indv_SD = [[0 for y in range(13)] for x in range(26)] 

DM_Year_Count = [[12 for y in range(13)] for x in range(26)] 
Pred_Weight_Matrix = [[0 for y in range(13)] for x in range(26)] 


#Probability_Homicide_=0.0
#Crime_Count=5133040

File_List_Input = ["Trainingdata_2001.csv",
			 "Trainingdata_2002.csv",
			 "Trainingdata_2003.csv",
			 "Trainingdata_2004.csv",
			 "Trainingdata_2005.csv",
			 "Trainingdata_2006.csv",
			 "Trainingdata_2007.csv",
			 "Trainingdata_2008.csv",
			 "Trainingdata_2009.csv",
			 "Trainingdata_2010.csv",
			 "Trainingdata_2011.csv",
			 "Trainingdata_2012.csv"]
			 
File_List_Test = ["Testing_Set_2013.csv",
			 "Testing_Set_2014.csv",
			 "Testing_Set_2015.csv"]
			 
File_List_Stat = ["Testing_Set_2013_Stat.csv",
			 "Testing_Set_2014_Stat.csv",
			 "Testing_Set_2015_Stat.csv"]
		
			 
#........................................ Reading the dataset.................................................#

def readfile():
	
	f=open("Crimes_latest.csv")
	csv_f=csv.reader(f)
	count_homicide=0
	count_arson=0
	count=0
	for row in csv_f:
		count=count+1
		if re.search(r'[2][0][1][3]',row[2]):
			print("2013 data")
		elif re.search(r'[2][0][1][4]',row[2]):
			print("2014 data")
		elif re.search(r'[2][0][1][5]',row[2]):
			print("2015 data")
		elif re.search(r'[2][0][1][6]',row[2]):
			print("2016 data")
		else:
			writefile_trainingdata(row)
	# print("Total count of crimes")
	print(count)
	f.close()
	
#....................................Appending to a new csv file..............................................#

def writefile_trainingdata(row):
	with open("Trainingdata.csv","a")as out_file:
		count=0
		while count<22:
			outstring=""
			outstring = outstring+row[count]+","
			out_file.write(outstring)
			#print(outstring)
			count=count+1
		outstring=outstring+"\n"
		out_file.write(outstring)		
	out_file.close()
	

	
#............................ Writing to a new CSV file after classification by primary type......................#

def WriteNewCSV(out_file,row):
	count=0
	while count<22:
		outstring=""
		if count == 8 or count == 9:
			if row[count] == "true" or row[count]== "false" or row[count] == "TRUE" or row[count]== "FALSE":			#So as to remove the comma in certain description making false positive cases
				outstring = ","+outstring+row[count]
				# print ("inside if.............................. ")
			else:
				outstring = outstring+row[count]						#So as to remove the comma in certain description making false positive cases
				# print ("inside else ")
		elif count != 0:
			outstring = ","+outstring+row[count]
		else:
			outstring = outstring+row[count]
		out_file.write(outstring)
		# print(outstring)
		count=count+1
	outstring=outstring+"\n"
	out_file.write(outstring)
	
#................................. NaiveBaivesfilter_addition .................................#
#.................................. Probability distribution of Distrcit for homicide..................................#

def MapNormalProb(NormVal):
	
	if NormVal <= -3.0: 
		NormVal = 0.0013
	elif NormVal > -3.0 and NormVal <= -2.5: 
		NormVal = 0.0049
	elif NormVal > -2.5 and NormVal <= -2.0: 
		NormVal = 0.0166
	elif NormVal > -2.0 and NormVal <= -1.5:
		NormVal = 0.0440
	elif NormVal > -1.5 and NormVal <= -1.0:
		NormVal = 0.0919
	elif NormVal > -1.0 and NormVal <= -0.5:
		NormVal = 0.1498
	elif NormVal > -0.5 and NormVal <= 0:
		NormVal = 0.1915
	elif NormVal > 0 and NormVal <= 0.5:
		NormVal = 0.1915
	elif NormVal > 0.5 and NormVal <= 1.0:
		NormVal = 0.1498
	elif NormVal > 1.0 and NormVal <= 1.5:
		NormVal = 0.0919
	elif NormVal > 1.5 and NormVal <= 2.0:
		NormVal = 0.0440
	elif NormVal > 2.0 and NormVal <= 2.5:
		NormVal = 0.0166
	elif NormVal > 2.5 and NormVal <= 3.0:
		NormVal = 0.0049
	elif NormVal > 3.0:
		NormVal = 0.0013
		
	return NormVal
	
def MapNormalVal(NormVal):
	
	if NormVal <= -2.0: 
		NormVal = 1
	elif NormVal > -2.0 and NormVal <= -1.5:
		NormVal = 2
	elif NormVal > -1.5 and NormVal <= -1.0:
		NormVal = 3
	elif NormVal > -1.0 and NormVal <= -0.5:
		NormVal = 4
	elif NormVal > -0.5 and NormVal <= 0:
		NormVal = 5
	elif NormVal > 0 and NormVal <= 0.5:
		NormVal = 6
	elif NormVal > 0.5 and NormVal <= 1.0:
		NormVal = 7
	elif NormVal > 1.0 and NormVal <= 1.5:
		NormVal = 8
	elif NormVal > 1.5 and NormVal <= 2.0:
		NormVal = 9
	elif NormVal > 2.0: 
		NormVal = 10
	
	Crime_Class_Count[NormVal] += 1
	return NormVal
	
def MapActualVal(NormVal):
	
	if NormVal == 1: 
		NormVal = -2.0
	elif NormVal == 2:
		NormVal = -1.5
	elif NormVal == 3:
		NormVal = -1.0
	elif NormVal == 4:
		NormVal = -0.5
	elif NormVal == 5 or NormVal == 6:
		NormVal = 0
	elif NormVal == 7:
		NormVal = 0.5
	elif NormVal == 8:
		NormVal = 1.0
	elif NormVal == 9:
		NormVal = 1.5
	elif NormVal == 10:
		NormVal = 2.0
	
	return NormVal
	
def limitOutlier(NormVal):
	
	if NormVal < -3.0:
		NormVal = -3.0
	elif NormVal > 3.0: 
		NormVal = 3.0

	return NormVal
	
def calculateProbability(x, mean, stdev):
	exponent = math.exp(-(math.pow((x*math.sqrt(stdev)),2)/(2*stdev)))
	denom = 2*math.pi*stdev
	return (1 / (math.sqrt(denom))) * exponent
	

def Analyze_Testing_Data():
	
	Month_ID = 0
	District_ID = 0
	Year_ID = 0

	#Analyzing Testing Data
	for year in range (1,4):
		with open(File_List_Test[year-1]) as Read_file:
			CSV_Read = csv.reader(Read_file)	
			for row in CSV_Read:
				if row[5] == "HOMICIDE":
					District_ID = int(row[11])											#conversion of string to int
					Month_ID = Month(row)
					Crime_Year_Count[District_ID][Month_ID][year+12] += 1
			print("Testing data file Read : ",File_List_Input[year-1])
		Read_file.close()
		
		with open(File_List_Stat[year-1],"w") as Write_file:
			row=""
			row += " "+","
			for month in range (1,13):
				row += str(month)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for month in range (1,13):
					row += str(Crime_Year_Count[district][month][year+12]) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
			Write_file.close()
		
	print("Homicide_Testing_Month_Stat writing finished")
	
	
def Probabilty_Homicide_district(District):
	
	year_count=0
	hom_count=0
	total_crime_count = 0
	total_hom_count = 0
	Month_ID = 0
	District_ID = 0
	Year_ID = 0
	Month_Count = 0
	row1 = {}

	# Counting the number of crimes in each year, across each month and district for year 2001-2012
	for year in range (1,13):
		with open(File_List_Input[year-1]) as Read_file:
			CSV_Read = csv.reader(Read_file)	
			for row in CSV_Read:
				if row[5] == "HOMICIDE":
					District_ID = int(row[11])											#conversion of string to int
					Month_ID = Month(row)
					Crime_Year_Count[District_ID][Month_ID][year] += 1
					Homicide_Count_Month[Month_ID] += 1
					hom_count += 1
				year_count += 1
			total_crime_count += year_count		
			total_hom_count += hom_count
			print("Input file Read : ",File_List_Input[year-1],"Crime Count = ",year_count," Homicide Count = ",hom_count)
			hom_count = 0
			year_count = 0
		Read_file.close()
	
	print("Input file reading finished , Total Count = ",total_crime_count)
	
	Analyze_Testing_Data()
	
	total_crime_count = 0
	
	#Iterations for prediction of each year
	for main_year in range (13,16):
		
		Crime_MD_Mean = 0 
		Crime_MD_SD = 0 
		District_Month_Count = 300
		#reset to intial values
		for district in range (1,26): 	# for every district		
			for month in range (1,13):
				Crime_MD_Count[district][month] = 0
				DM_Year_Count[district][month] = 12
				Crime_MD_Indv_Mean[district][month] = 0
				Crime_MD_Indv_SD[district][month] = 0
				Crime_MD_Norm[district][month] = 0
		#Finding count across month/district upto the current year
		for district in range (1,26): 	# for every district		
			for month in range (1,13):
				for year in range (1,main_year):
					Crime_MD_Count[district][month] += Crime_Year_Count[district][month][year]
		#Calculating mean , Standard deviation and leaving out 0 frequency values			
		for district in range (1,26): 	# for every district		
			for month in range (1,13):
				if(Crime_MD_Count[district][month] != 0):
					Crime_MD_Mean += Crime_MD_Count[district][month]
				else:
					District_Month_Count -= 1
			
		Crime_MD_Mean /= District_Month_Count					# 300 or less possibilities, neglecting 0
		
		for district in range (1,26): 	# for every district		
			for month in range (1,13):
				if(Crime_MD_Count[district][month] != 0):
					Crime_MD_SD += (Crime_MD_Count[district][month]  - Crime_MD_Mean)**2
				
		Crime_MD_SD /= District_Month_Count					# 300 or less possibilities, neglecting 0
		
		print("Mean = ",Crime_MD_Mean,"SD = ",Crime_MD_SD)
		
		#Calculating mean and SD for each district month combinations over the years upto current year
		for district in range (1,26): 	# for every district		
			for month in range (1,13):
				for year in range (1,main_year):
					Crime_MD_Indv_Mean[district][month] += Crime_Year_Count[district][month][year]
					if Crime_MD_Count[district][month] == 0:
						DM_Year_Count[district][month] -= 1
				if DM_Year_Count[district][month] != 0:
					Crime_MD_Indv_Mean[district][month] /= DM_Year_Count[district][month] 
				else:
					Crime_MD_Indv_Mean[district][month] = 0

				for year in range (1,main_year):
					if Crime_MD_Count[district][month] != 0:
						Crime_MD_Indv_SD[district][month] += (Crime_Year_Count[district][month][year]  - Crime_MD_Indv_Mean[district][month])**2
				if DM_Year_Count[district][month] != 0:
					Crime_MD_Indv_SD[district][month] /= DM_Year_Count[district][month] 
				else:
					Crime_MD_Indv_SD[district][month] = 0
		
		#Normalizing and mapping to classes 1-10
		for district in range (1,26): 	# for every district
			for month in range (1,13):
				if Crime_MD_Count[district][month] != 0:
					Crime_MD_Norm[district][month] = MapNormalVal((Crime_MD_Count[district][month] - Crime_MD_Mean) / math.sqrt(Crime_MD_SD))	
				else:
					Crime_MD_Norm[district][month] = 0
		#Calculating the class probabilty
		for class_num in range (1,11):
			if Crime_Class_Count[class_num] == 0:
				Crime_Class_Count[class_num] = 1
			Crime_Class_Prob[class_num] = Crime_Class_Count[class_num]/District_Month_Count			
		#Calculating conditional probabilty district|class and month|class
		for class_num in range (1,11):
			for district in range (1,26): 	# for every district	
				count = 0
				for month in range (1,13):
					if Crime_MD_Norm[district][month] == class_num:
						count += 1
				Crime_District_Cond_Prob[district][class_num] = count/Crime_Class_Count[class_num]
			
			for month in range (1,13):
				count = 0
				for district in range (1,26): 	# for every district	
					if Crime_MD_Norm[district][month] == class_num:
						count += 1
				Crime_Month_Cond_Prob[month][class_num] = count/Crime_Class_Count[class_num]
		#Calculating final probability for each class 1-10 in each month and district combination, and choosing the class with high prob
		for district in range (1,26): 	# for every district
			for month in range (1,13):
				greatest_prob = 0
				for class_num in range (1,11):
					Crime_Final_Prob[district][month][class_num] = Crime_District_Cond_Prob[district][class_num] * Crime_Month_Cond_Prob[month][class_num] * Crime_Class_Prob[class_num]
					if Crime_Final_Prob[district][month][class_num] > greatest_prob:
						Crime_Final_Class[district][month] = class_num
						greatest_prob = Crime_Final_Prob[district][month][class_num] 
		#Using class number to map to actual value based on distribution of class over district month combination over years
		for class_num in range (1,11):		
			SD_mult_val = 0
			round_val = 0
			ceil_val = 0
			SD_mult_val = MapActualVal(class_num)
			for district in range (1,26): 	# for every district
				for month in range (1,13):		
					if DM_Year_Count[district][month] != 0:
						Crime_Class_Pred[district][month][class_num] = round(((SD_mult_val*math.sqrt(Crime_MD_Indv_SD[district][month])) + Crime_MD_Indv_Mean[district][month])) 
					else:
						Crime_Class_Pred[district][month][class_num] = 0
		#Updating the final predictions and adjusting using weight
		for district in range (1,26): 	# for every district
			for month in range (1,13):
				Crime_Final_Pred[district][month] = Crime_Class_Pred[district][month][Crime_Final_Class[district][month]] + Pred_Weight_Matrix[district][month]
				if Crime_Final_Pred[district][month] < 0:
					Crime_Final_Pred[district][month] = 0
		
		for district in range (1,26): 	# for every district
			for month in range (1,13):
				Crime_MD_Max[district][month] = 0
				Crime_MD_Min[district][month] = 9999999
				for year in range (1,13):
					if Crime_Year_Count[district][month][year] > Crime_MD_Max[district][month]:
						Crime_MD_Max[district][month] = Crime_Year_Count[district][month][year]
					
					if Crime_Year_Count[district][month][year] < Crime_MD_Min[district][month]:
						Crime_MD_Min[district][month] = Crime_Year_Count[district][month][year]
		#Updating the prediction weight matrix
		for district in range (1,26): 	# for every district
			for month in range (1,13):
				Pred_Weight_Matrix[district][month] += Crime_Year_Count[district][month][main_year] - Crime_Final_Pred[district][month]

		
		print("Prob calc finished before year ",main_year)
		
		File_String = " "
		File_String = str(main_year)+"_Homicide_District_Month_Stat.csv"
		with open(File_String,"w") as Write_file:
			row=""
			row += " "+","
			for month in range (1,13):
				row += str(month)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for month in range (1,13):
					row += str(Crime_MD_Count[district][month]) + ","
				row += str(Crime_MD_Mean) + ","
				row += str(Crime_MD_SD) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
		Write_file.close()
		print("Homicide_District_Month_Stat writing finished",main_year)
		
		File_String = " "
		File_String = str(main_year)+"_Homicide_District_Month_Norm.csv"
		with open(File_String,"w") as Write_file:
			row=""
			row += " "+","
			for month in range (1,13):
				row += str(month)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for month in range (1,13):
					row += str(Crime_MD_Norm[district][month]) + ","
				#row += str(Crime_MD_Mean[district]) + ","
				#row += str(Crime_MD_SD[district]) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
		Write_file.close()
		
		print("Homicide_District_Month_Norm writing finished",main_year)
		File_String = " "		
		File_String = str(main_year)+"_Homicide_District_Cond_Prob.csv"
		with open(File_String,"w") as Write_file:
			row=""
			row += " "+","
			for class_num in range (1,11):
				row += str(class_num)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for class_num in range (1,11):
					row += str(Crime_District_Cond_Prob[district][class_num]) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
		Write_file.close()
		
		print("Homicide_Month_Cond_Prob writing finished",main_year)	
		File_String = " "		
		File_String = str(main_year)+"_Homicide_Month_Cond_Prob.csv"
		with open(File_String,"w") as Write_file:
			row=""
			row += " "+","
			for class_num in range (1,11):
				row += str(class_num)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for month in range (1,13):
				row+= str(month)+ ","
				for class_num in range (1,11):
					row += str(Crime_Month_Cond_Prob[month][class_num]) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
		Write_file.close()
		
		print("Homicide_Month_Cond_Prob writing finished",main_year)
		File_String = " "	
		File_String = str(main_year)+"_Homicide_Final_Prob.csv"
		with open(File_String,"w") as Write_file:
			row=""
			row += "District"+","
			row += "Month"+","
			row += " "+","
			for class_num in range (1,11):
				row += str(class_num)+","
			row += " "+","
			row += "Pred_Class"+","
			row += "Pred_Val"+","
			row += "Act_Val"+","
			row += '\n'
			Write_file.write(row)
			
			row=""

			for district in range (1,26):
				for month in range (1,13):
					row+= str(district)+ ","
					row+= str(month)+ ","
					row += " "+","
					for class_num in range (1,11):
						row += str(Crime_Final_Prob[district][month][class_num]) + ","
					row += " "+","
					row += str(Crime_Final_Class[district][month]) + ","
					row += str(Crime_Final_Pred[district][month]) + ","
					row += str(Crime_Year_Count[district][month][main_year]) + ","
					row += '\n'
					Write_file.write(row)
					row = ""
		Write_file.close()
		
		print("Homicide_Final_Prob writing finished",main_year)	
		File_String = " "	
		File_String = str(main_year)+"_Homicide_Final_Class_DM_Format.csv"
		with open(File_String,"w") as Write_file:
			row=""
			row += " "+","
			for month in range (1,13):
				row += str(month)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for month in range (1,13):
					row += str(Crime_Final_Class[district][month]) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
		Write_file.close()
		
		print("Homicide_Final_Class_DM_Format writing finished",main_year)	
		File_String = " "	
		File_String = str(main_year)+"_Homicide_Final_Prediction.csv"
		with open(File_String,"w") as Write_file:
			row=""
			row += " "+","
			for month in range (1,13):
				row += str(month)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for month in range (1,13):
					row += str(Crime_Final_Pred[district][month]) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
		Write_file.close()
	
		print("Homicide_Final_Prediction writing finished",main_year)		

		File_String = " "		
		File_String = str(main_year)+"_Homicide_Pred_Weight.csv"
		with open(File_String,"w") as Write_file:
			row=""
			row += " "+","
			for month in range (1,13):
				row += str(month)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for month in range (1,13):
					row += str(Pred_Weight_Matrix[district][month]) + ","
				#row += str(Crime_MD_Mean[district]) + ","
				#row += str(Crime_MD_SD[district]) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
		Write_file.close()
		
		print("Homicide_Pred_Weight writing finished",main_year)
		
		File_String = " "		
		File_String = str(main_year)+"_Homicide_District_Month_Mean.csv"
		with open(File_String,"w") as Write_file:
			row=""
			row += " "+","
			for month in range (1,13):
				row += str(month)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for month in range (1,13):
					row += str(Crime_MD_Indv_Mean[district][month]) + ","
				#row += str(Crime_MD_Mean[district]) + ","
				#row += str(Crime_MD_SD[district]) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
		Write_file.close()
		
		print("Homicide_District_Month_Mean writing finished",main_year)
		File_String = " "		
		File_String = str(main_year)+"_Homicide_District_Month_SD.csv"
		with open(File_String,"w") as Write_file:		
			row=""
			row += " "+","
			for month in range (1,13):
				row += str(month)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for month in range (1,13):
					row += str(Crime_MD_Indv_SD[district][month]) + ","
				#row += str(Crime_MD_Mean[district]) + ","
				#row += str(Crime_MD_SD[district]) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
		Write_file.close()
		
		print("Homicide_District_Month_SD writing finished",main_year)
	

	
#.................................. Probability distribution of month for homicide..................................#

def Probabilty_Homicide_Month(Month_homicide,District_month):

	count=0
	Read_file=open("HOMICIDE.csv")
	csv_f=csv.reader(Read_file)
	for count in range(0,len(Month_homicide)):
		District_month[count] = Month_homicide[count]											
		Probabilty_Homicide_Month_[District_month[count]]=Probabilty_Homicide_Month_[District_month[count]]+1
		count=count+1
	Read_file.close()
	for x in range (1,13):
		Probabilty_Homicide_Month_[x]=Probabilty_Homicide_Month_[x]/count
	
#............................Month calculation..................................#

def Month(row):
	date_int=0
	if re.search(r'[/]',row[2]):
		date=row[2].split("/")
		#print("The date is ",date[0])
	elif re.search(r'[-]',row[2]):
		date=row[2].split("-")
		#print("The date is ",date[0])
	date_int = int (date[0])
	#print("The month is ",date_int)
	return date_int
	
def Year(row):
	year = re.search(r'\d{4}',row[2])
	#print(year.group())
	return int(year.group())


#....................................The main function....................................#

def main():
#............................ preprocesing - The dataset for training in now put into a new file.............................#

	# readfile() 
#....................................................	Split the crimes based on Primary types....................................................#
	
	# f=open("trainingdata.csv")
	# csv_f=csv.reader(f)
	# count_homicide=1
	# count_arson=0
	# count_criminal_damage=1
	# count=0
	
	# for row in csv_f:
		# count=count+1
		# print(row[5])
		# if row[5] == 'ARSON':
			# count_arson=count_arson+1
			# with open("ARSON.csv","a")as out_file:
				# WriteNewCSV(out_file,row)
			# out_file.close()
		# elif row[5] == 'HOMICIDE':
			# #print("homicide count is ",count_homicide)
			# with open("HOMICIDE.csv","a")as out_file:
				# WriteNewCSV(out_file,row)
				# count_homicide=count_homicide+1
			# out_file.close()
		# if row[5] == 'CRIMINAL DAMAGE':
			# print("count_criminal_damage count is ",count_criminal_damage)
			# with open("CRIMINAL DAMAGE.csv","a")as out_file:
				# WriteNewCSV(out_file,row)
				# count_criminal_damage=count_criminal_damage+1
			# out_file.close()
		
	# print("split data complete")
	# print("count_criminal_damage count is ",count_criminal_damage)
	# f.close()
#................................... Probability for Homicide..................................#
	# count=0
	# f=open("trainingdata.csv")
	# csv_f=csv.reader(f)
	# for row in csv_f:
		# count=count+1
	count_homicide=6112
	#Probability_Homicide_=count_homicide/Crime_Count
	

#................................... District Probability Distribution for Homicide..................................#

	
	# NaiveBaivesfilter_Homicide_addition(count_homicide)
	# print("NaiveBaivesfilter is complete")
	District = [0 for x in range(count_homicide)]
	Probabilty_Homicide_district(District)
	#for x in range(1,26):
		#print("The probabilty of homicide district ",x," is: ",Probabilty_Homicide_district_[x])

#................................... Month Probability Distribution for Homicide..................................#

	#date_int = 0
	#Month_homicide=[0 for x in range (count_homicide)]
	#District_month = [0 for x in range(count_homicide)]
	#ReqProb_Dist_Month = [[0 for x in range(13)] for y in range(26)] 
	#count_date_=0
	#Read_Date=open("HOMICIDE.csv")
	#csv_f=csv.reader(Read_Date)
	#for row in csv_f:
		#Month_homicide[count_date_]=Month(row,count_date_)
		# print("The month is ",Month_homicide[count_date_])
		#count_date_=count_date_+1
	#Read_Date.close()
	#Probabilty_Homicide_Month(Month_homicide,District_month)
	#for x in range(1,13):
		#print("The probabilty of homicide  month ",x," is: ",Probabilty_Homicide_Month_[x])
	#print("NaiveBaivesfilter for month is complete")
	#for x in range (1,26):
		#for y in range (1,13):
			#ReqProb_Dist_Month[x][y] = Probabilty_Homicide_Month_[y]*Probabilty_Homicide_district_[x]*Probability_Homicide_
			#print(ReqProb_Dist_Month[x][y])
	#for x in range (1,13):
		#print("The Crime for Year ",x,"is ",Crime_Count_Year[x])
	#for y in range (1,13):
		#print("The Crime for Month ",y,"is ",Crime_Count_Month[y])
	#for z in range (1,26):	
		#print("The Crime for District ",z,"is ",Crime_Count_District[z])
	#for x in range (1,13):
		#print("The Crime for Year ",x)
		#for y in range (1,13):
			#print("in Month ",y)
			#for z in range (1,26):	
				#print("for district ",z,"is ",Crime_Count[x][y][z])
#................................. Main function call .................................#	

main()
