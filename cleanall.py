#Google Trends all files Data Cleaning
import os.path
import csv
import re
import sys
import glob

fileDir = ''
exportFile = open('../cleaned_premier_data/all_cleaned.csv', 'w+')
path =r'../Premier_Data' 
allFiles = glob.glob(path + "/*.csv")

teamNo = 0
hRange = range(0,56)

for currFile in allFiles:
	print(currFile)
	fileDir = open(currFile,'rU')
	reader = csv.reader(fileDir)
	print(reader)
	teamNo += 1
	search_term = ''
	ndoc = [None] * 6
	head = 0

	for cdoc in reader:
		print(cdoc)
		if head in hRange:
			if teamNo == 1 and head ==4:
				ndoc[0] = 'Week'
				ndoc[1] = 'Start'
				ndoc[2] = 'End'
				ndoc[3] = 'Team Index'
				ndoc[4] = 'Google Trends Index'
				ndoc[5] = 'Search term'

				output = ','.join(ndoc) + '\n'
				exportFile.write(output)

			if head == 4:
				search_term = cdoc[1]
			elif head > 4:
				days = cdoc[0].split(" - ")
				ndoc[0] = str(head - 4)
				ndoc[1] = days[0]
				ndoc[2] = days[1]
				ndoc[3] = str(teamNo)
				ndoc[4] = cdoc[1]
				ndoc[5] = search_term
				output = ','.join(ndoc) + '\n'
				exportFile.write(output)

		else:
			continue
		
		head += 1

exportFile.close()