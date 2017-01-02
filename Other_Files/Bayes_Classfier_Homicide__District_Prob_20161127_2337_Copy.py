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
Crime_Year_Count = [[[0 for z in range(13)] for y in range(13)] for x in range(26)]
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
			 "Testing_Set_2012.csv",
			 "Testing_Set_2015.csv"]
		
			 
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
	
	year_count=0
	hom_count=0
	total_crime_count = 0
	total_hom_count = 0
	Month_ID = 0
	District_ID = 0
	Year_ID = 0
	Month_Count = 0
	row1 = {}
	District_Month_Count = 300
	
	
	Crime_MD_Mean = 0 
	Crime_MD_SD = 0 

	for year in range (1,13):
	#for year in range (1,2):
		with open(File_List_Input[year-1]) as Read_file:
		#with open("Input_Test.csv") as Read_file:
			CSV_Read = csv.reader(Read_file)	
			for row in CSV_Read:
				if row[5] == "HOMICIDE":
					District_ID = int(row[11])											#conversion of string to int
					Month_ID = Month(row)
					#print("District ID = ",District_ID," Month ID = ",Month_ID)
					Crime_MD_Count[District_ID][Month_ID] += 1
					Crime_Year_Count[District_ID][Month_ID][year] += 1
					Homicide_Count_Month[Month_ID] += 1
					#print("Crime_Count[",Month_ID,"][",District_ID,"][",year,"] = ",Crime_Count[Month_ID][District_ID][year])
					hom_count += 1
				year_count += 1
			total_crime_count += year_count		
			total_hom_count += hom_count
			print("Input file Read : ",File_List_Input[year-1],"Crime Count = ",year_count," Homicide Count = ",hom_count)
			hom_count = 0
			year_count = 0
		Read_file.close()
	
	print("Input file reading finished , Total Count = ",total_crime_count)
	
	
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
	District_Month_Count = 300
	
	
	Crime_MD_Mean = 0 
	Crime_MD_SD = 0 

	for year in range (1,13):
	#for year in range (1,2):
		with open(File_List_Input[year-1]) as Read_file:
		#with open("Input_Test.csv") as Read_file:
			CSV_Read = csv.reader(Read_file)	
			for row in CSV_Read:
				if row[5] == "HOMICIDE":
					District_ID = int(row[11])											#conversion of string to int
					Month_ID = Month(row)
					#print("District ID = ",District_ID," Month ID = ",Month_ID)
					Crime_MD_Count[District_ID][Month_ID] += 1
					Crime_Year_Count[District_ID][Month_ID][year] += 1
					Homicide_Count_Month[Month_ID] += 1
					#print("Crime_Count[",Month_ID,"][",District_ID,"][",year,"] = ",Crime_Count[Month_ID][District_ID][year])
					hom_count += 1
				year_count += 1
			total_crime_count += year_count		
			total_hom_count += hom_count
			print("Input file Read : ",File_List_Input[year-1],"Crime Count = ",year_count," Homicide Count = ",hom_count)
			hom_count = 0
			year_count = 0
		Read_file.close()
	
	print("Input file reading finished , Total Count = ",total_crime_count)
	
	total_crime_count = 0
	"""
	for month in range (1,13):
		for district in range (1,26):
			for year in range (1,13):
			#for year in range (1,2):
				Month_Count += Crime_Count[month][district][year]
				#print("Print_Count[",month,"][",district,"][",year,"] = ",Crime_Count[month][district][year]," Month Count",Month_Count)
		print("Month - ",month," Count = ",Month_Count)	
		total_count += Month_Count
		Month_Count = 0

	print("Month print finished , Total Count = ",total_count)
	"""	
	
	for month in range (1,13):
		Homicide_Month_Prob[month] = Homicide_Count_Month[month]/total_hom_count
	"""	
	for district in range (1,26): 	# for every district		
		for month in range (1,13):
			Crime_MD_Count[district][month] /= 12
	"""
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
	
	for district in range (1,26): 	# for every district		
		for month in range (1,13):
			for year in range (1,13):
				#if(Crime_MD_Count[district][month] != 0):
				Crime_MD_Indv_Mean[district][month] += Crime_Year_Count[district][month][year]
				if Crime_MD_Count[district][month] == 0:
					DM_Year_Count[district][month] -= 1
				#else:
					#District_Month_Count -= 1
			if DM_Year_Count[district][month] != 0:
				Crime_MD_Indv_Mean[district][month] /= DM_Year_Count[district][month] 
			else:
				Crime_MD_Indv_Mean[district][month] = 0
	#Crime_MD_Mean /= District_Month_Count					# 300 or less possibilities, neglecting 0
	
	#for district in range (1,26): 	# for every district		
		#for month in range (1,13):
			for year in range (1,13):
				if Crime_MD_Count[district][month] != 0:
					Crime_MD_Indv_SD[district][month] += (Crime_Year_Count[district][month][year]  - Crime_MD_Indv_Mean[district][month])**2
			if DM_Year_Count[district][month] != 0:
				Crime_MD_Indv_SD[district][month] /= DM_Year_Count[district][month] 
			else:
				Crime_MD_Indv_SD[district][month] = 0
	
	for district in range (1,26): 	# for every district
		for month in range (1,13):
			if Crime_MD_Count[district][month] != 0:
				Crime_MD_Norm[district][month] = MapNormalVal((Crime_MD_Count[district][month] - Crime_MD_Mean) / math.sqrt(Crime_MD_SD))	
			else:
				Crime_MD_Norm[district][month] = 0
		
	for class_num in range (1,11):
		if Crime_Class_Count[class_num] == 0:
			Crime_Class_Count[class_num] = 1
		Crime_Class_Prob[class_num] = Crime_Class_Count[class_num]/District_Month_Count
		#print("Crime_Class_Prob[",class_num,"] = ",Crime_Class_Prob[class_num]," Crime_Class_Count[",class_num,"] = ",Crime_Class_Count[class_num]," District_Month_Count = ",District_Month_Count)
		
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
			
	for district in range (1,26): 	# for every district
		for month in range (1,13):
			greatest_prob = 0
			for class_num in range (1,11):
				Crime_Final_Prob[district][month][class_num] = Crime_District_Cond_Prob[district][class_num] * Crime_Month_Cond_Prob[month][class_num] * Crime_Class_Prob[class_num]
				if Crime_Final_Prob[district][month][class_num] > greatest_prob:
					Crime_Final_Class[district][month] = class_num
					greatest_prob = Crime_Final_Prob[district][month][class_num] 
					
	for class_num in range (1,11):		
		SD_mult_val = 0
		round_val = 0
		ceil_val = 0
		SD_mult_val = MapActualVal(class_num)
		for district in range (1,26): 	# for every district
			for month in range (1,13):		
				if DM_Year_Count[district][month] != 0:
					Crime_Class_Pred[district][month][class_num] = round(((SD_mult_val*math.sqrt(Crime_MD_Indv_SD[district][month])) + Crime_MD_Indv_Mean[district][month]))#/DM_Year_Count[district][month])
				else:
					Crime_Class_Pred[district][month][class_num] = 0
		#round_val = round(Crime_Class_Pred[class_num],0)
		#ceil_val = math.ceil(Crime_Class_Pred[class_num])
		#print("Crime_Class_Pred[",class_num,"] = ",Crime_Class_Pred[class_num])#," round = ",round_val," ceil = ",ceil_val)
		
	for district in range (1,26): 	# for every district
		for month in range (1,13):
			Crime_Final_Pred[district][month] = Crime_Class_Pred[district][month][Crime_Final_Class[district][month]]
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
				
	"""
	for year in range (1,13):
	#for year in range (1,2):
		#Crime_MD_Norm[month][district][year] = limitOutlier(Crime_MD_Norm[month][district][year])
		if Crime_MD_Mean[month][district]!= 0  and Crime_MD_SD[month][district]!=0:#Crime_MD_Norm[month][district][year]!=0:
			#Crime_Ind_Prob[month][district][year] = calculateProbability(Crime_MD_Norm[month][district][year],Crime_MD_Mean[month][district],Crime_MD_SD[month][district])
			Crime_Ind_Prob[month][district][year] = MapNormalProb(Crime_MD_Norm[month][district][year])
			Crime_Prob[month][district] += Crime_Ind_Prob[month][district][year]
			#Crime_Prob[month][district] *= calculateProbability(Crime_MD_Norm[month][district][year],Crime_MD_Mean[month][district],Crime_MD_SD[month][district])
			#Crime_MD_Norm[y][x] = MapNormalVal(Crime_MD_Norm[y][x])			
		else:
			Crime_Ind_Prob[month][district][year] = 0
			Crime_Prob[month][district] += Crime_Ind_Prob[month][district][year]
			#if Is_Outlier == True:
				#print("Outlier_Count[",month,"][",district,"][",year,"] = ",Crime_Count[month][district][year])
			#print("Normal_Outlier_Value = ",Crime_MD_Norm[month][district][year])
			#Crime_Ind_Prob[month][district][year] = 1
			#Crime_Prob[month][district] *= Crime_Ind_Prob[month][district][year]
		#print("Crime_Prob in year ",year," , Month ",month,", District  ",district," is = ",Crime_Prob[month][district]," Exp Prob = ",Calc_Prob)
	
	Crime_Prob[month][district] /= 12
	"""
	print("Prob calc finished")
	
	with open("Homicide_District_Month_Stat.csv","w") as Write_file:
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
	
	print("Homicide_District_Month_Stat writing finished")
	
	with open("Homicide_District_Month_Norm.csv","w") as Write_file:
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
	
	print("Homicide_District_Month_Norm writing finished")
	
	with open("Homicide_District_Cond_Prob.csv","w") as Write_file:
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
	
	print("Homicide_Month_Cond_Prob writing finished")	
	
	with open("Homicide_Month_Cond_Prob.csv","w") as Write_file:
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
	
	print("Homicide_Month_Cond_Prob writing finished")
	
	with open("Homicide_Final_Prob.csv","w") as Write_file:
		row=""
		row += "District"+","
		row += "Month"+","
		row += " "+","
		for class_num in range (1,11):
			row += str(class_num)+","
		row += " "+","
		row += "Pred_Class"+","
		row += "Min"+","
		row += "Max"+","
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
				row += str(Crime_MD_Min[district][month]) + ","
				row += str(Crime_MD_Max[district][month]) + ","
				row += '\n'
				Write_file.write(row)
				row = ""
	Write_file.close()
	
	print("Homicide_Final_Prob writing finished")	
	
	with open("Homicide_Final_Class_DM_Format.csv","w") as Write_file:
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
	
	print("Homicide_Final_Class_DM_Format writing finished")	
	
	with open("Homicide_Final_Prediction.csv","w") as Write_file:
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
	
	print("Homicide_Final_Prediction writing finished")		
	
	with open("Homicide_District_Month_Mean.csv","w") as Write_file:
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
	
	print("Homicide_District_Month_Mean writing finished")
	
	with open("Homicide_District_Month_SD.csv","w") as Write_file:
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
	
	print("Homicide_District_Month_SD writing finished")
	
	"""
	for month in range (1,13):
		with open(File_List_Output_Stat[month-1],"w") as Write_file:
			row=""
			row += " "+","
			for year in range (1,13):
				row += str(year)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for year in range (1,13):
					row += str(Crime_Count[month][district][year]) + ","
				row += str(Crime_MD_Mean[month][district]) + ","
				row += str(Crime_MD_SD[month][district]) + ","
				row += '\n'
				Write_file.write(row)
				#print("3",row)
				row = ""
				#print("Save_Count[",month,"][",district,"][",year,"] = ",Crime_Count[month][district][year]," Month Count",Month_Count)
		Write_file.close()
	
	print("Output file Stat writing finished")
	
	for month in range (1,13):
		with open(File_List_Output_Norm[month-1],"w") as Write_file:
			row=""
			row += " "+","
			for year in range (1,13):
				row += str(year)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for year in range (1,13):
					row += str(Crime_MD_Norm[month][district][year]) + ","
				row += str(Crime_MD_Mean[month][district]) + ","
				row += str(Crime_MD_SD[month][district]) + ","
				row += '\n'
				Write_file.write(row)
				#print("3",row)
				row = ""
				#print("Save_Count[",month,"][",district,"][",year,"] = ",Crime_Count[month][district][year]," Month Count",Month_Count)
		Write_file.close()
	
	print("Output file Norm writing finished")
	
	for month in range (1,13):
		with open(File_List_Output_Prob[month-1],"w") as Write_file:
			row=""
			row += " "+","
			for year in range (1,13):
				row += str(year)+","
			row += '\n'
			Write_file.write(row)
			row = ""
			for district in range (1,26):
				row+= str(district)+ ","
				for year in range (1,13):
					row += str(Crime_Ind_Prob[month][district][year]) + ","
				row += str(Crime_MD_Mean[month][district]) + ","
				row += str(Crime_MD_SD[month][district]) + ","
				row += '\n'
				Write_file.write(row)
				#print("3",row)
				row = ""
				#print("Norm Mean[",month,"][",district,"] = ",Crime_MD_Mean[month][district],"SD[",month,"][",district,"] = ",Crime_MD_SD[month][district])
		Write_file.close()
	
	print("Output file Indv Prob writing finished")
	"""


	
	"""	
	for x in range (1,26):
		div_count = 12
		for y in range (1,13):	
			if(Crime_Count[y][x] == 0):
				div_count -= 1
			else:
				Crime_MD_Mean[x] += Crime_Count[y][x]
		if(div_count != 0):
			Crime_MD_Mean[x] /= div_count
		else:
			Crime_MD_Mean[x] = 0
		print("Mean of row ",x," is ",Crime_MD_Mean[x],"and Div is ",div_count)
		for y in range (1,13):
			if(Crime_Count[y][x] != 0):
				Crime_MD_SD[x] += (Crime_Count[y][x] - Crime_MD_Mean[x])**2
		
		if(div_count != 0):
			Crime_MD_SD[x] /= div_count
		else:
			Crime_MD_SD[x] = 0
		
		print("SD of row ",x," is ",Crime_MD_SD[x],"and Div is ",div_count)
		
		for y in range (1,13):
			if Crime_MD_Mean[x]!= 0  and Crime_MD_SD[x]!=0:
				Crime_MD_Norm[y][x] = ((Crime_Count[y][x] - Crime_MD_Mean[x]) / Crime_MD_SD[x])
				#print("Crime_MD_Norm",y,"-",x," ",Crime_MD_Norm[y][x])
				#Crime_MD_Norm[y][x] = MapNormalVal(Crime_MD_Norm[y][x])			
			else:
				Crime_MD_Norm[y][x] = 0
		
		for y in range (1,13):
			Is_Outlier = False
			Is_Outlier = checkOutlier(Crime_MD_Norm[y][x])
			if Is_Outlier == True and Crime_MD_Norm[y][x]!=0:
				Crime_Prob[y][x] = calculateProbability(Crime_MD_Norm[y][x],Crime_MD_Mean[x],Crime_MD_SD[x])
				#print("Crime_Prob",y,"-",x," ",Crime_Prob[y][x])
				#Crime_MD_Norm[y][x] = MapNormalVal(Crime_MD_Norm[y][x])			
			else:
				Crime_Prob[y][x] = 0			
	
				
	with open("Homicide_Stats_Testing_2013.csv","w") as Write_file:
		row=""
		row += " "+","
		for x in range (1,13):
			row += str(x)+","
		row += '\n'
		Write_file.write(row)
		row = ""
		for y in range (1,26):
			row+= str(y)+ ","
			for z in range (1,13):
				row += str(Crime_Count[z][y]) + ","
			row += str(Crime_MD_Mean[y]) + ","
			row += str(Crime_MD_SD[y]) + ","
			row += '\n'
			Write_file.write(row)
			#print("3",row)
			row = ""
	Write_file.close()
	
	with open("Homicide_Norm_Testing_2013.csv","w") as Write_file:
		row=""
		row += " "+","
		for x in range (1,13):
			row += str(x)+","
		row += '\n'
		Write_file.write(row)
		row = ""
		for y in range (1,26):
			row+= str(y)+ ","
			for z in range (1,13):
				row += str(Crime_MD_Norm[z][y]) + ","
			row += str(Crime_MD_Mean[y]) + ","
			row += str(Crime_MD_SD[y]) + ","
			row += '\n'
			Write_file.write(row)
			#print("3",row)
			row = ""
	Write_file.close()
	
	with open("Homicide_Prob_Testing_2013.csv","w") as Write_file:
		row=""
		row += " "+","
		for x in range (1,13):
			row += str(x)+","
		row += '\n'
		Write_file.write(row)
		row = ""
		for y in range (1,26):
			row+= str(y)+ ","
			for z in range (1,13):
				row += str(Crime_Prob[z][y]) + ","
			row += str(Crime_MD_Mean[y]) + ","
			row += str(Crime_MD_SD[y]) + ","
			row += '\n'
			Write_file.write(row)
			#print("3",row)
			row = ""
	Write_file.close()
	"""	

	
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
