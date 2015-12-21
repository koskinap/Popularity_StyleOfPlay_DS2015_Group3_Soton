#Google Trends all files Data Cleaning
import os.path
import csv
import sys
import glob

fileDir = ''
exportFile = open('../cleaned_premier_data/cleaned_gtrends.csv', 'w+')
path =r'../Premier_Data' 
allFiles = glob.glob(path + "/*.csv")

teamNo = 0
hRange = range(0,56)

for currFile in allFiles:

	fileDir = open(currFile,'rU')
	reader = csv.reader(fileDir)
	teamNo += 1
	search_term = ''
	ndoc = [None] * 6
	head = 0

	for cdoc in reader:
		if head in hRange:
			if teamNo == 1 and head ==4:
				ndoc = ['Week','Start Date','End Date','TeamIndex','Google Trends Index','Search Term']
				output = ','.join(ndoc) + '\n'
				exportFile.write(output)

			if head == 4:
				search_term = cdoc[1]
			elif head > 4:
				days = cdoc[0].split(" - ")
				ndoc = [str(head - 4),days[0],days[1],str(teamNo),cdoc[1],search_term]
				output = ','.join(ndoc) + '\n'
				exportFile.write(output)
		else:
			continue		
		head += 1

exportFile.close()