#Google Trends Data Cleaning
import os.path
import csv
import re
import sys

fileDir = open('../Premier_Data/arsenalfc.csv','rU')
exportFile = open('../cleaned_premier_data/arsenalfc_cleaned.csv', 'w+')

reader = csv.reader(fileDir)

search_term = ''
ndoc = [None] * 5

print(type(reader))

teamNo = 1
head = 0

hRange = range(0,56)
for cdoc in reader:
	if head in hRange:
		if head == 4:
			ndoc[0] = 'Week'
			ndoc[1] = 'Start'
			ndoc[2] = 'End'
			ndoc[3] = 'Team Index'
			ndoc[4] = 'Google Trends Index'

			output = ','.join(ndoc) + '\n'
			exportFile.write(output)

		elif head > 4:
			days = cdoc[0].split(" - ")
			ndoc[0] = str(head - 4)
			ndoc[1] = days[0]
			ndoc[2] = days[1]
			ndoc[3] = str(teamNo)
			ndoc[4] = cdoc[1]
			output = ','.join(ndoc) + '\n'
			exportFile.write(output)

		head += 1
	else:
		head += 1
		continue

fileDir.close()
exportFile.close()