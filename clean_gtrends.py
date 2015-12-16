#Google Trends Data Cleaning
import os.path
import csv
import sys

fileDir = open('../Premier_Data/chelseafc.csv','rU')
exportFile = open('../cleaned_premier_data/chelseafc_cleaned.csv', 'w+')

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
			ndoc = ['Week','Start','End','TeamIndex','Google Trends Index']

			output = ','.join(ndoc) + '\n'
			exportFile.write(output)

		elif head > 4:
			days = cdoc[0].split(" - ")
			ndoc = [str(head - 4),days[0],days[1],str(teamNo),cdoc[1]]

			output = ','.join(ndoc) + '\n'
			exportFile.write(output)

		head += 1
	else:
		head += 1
		continue

fileDir.close()
exportFile.close()