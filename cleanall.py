#Google Trends Data Cleaning
import os.path
import csv
import re
import sys
import glob
#import pandas as pd

#fileDir = open('../Premier_Data/arsenalfc.csv','rU')
fileDir = ''
exportFile = open('../cleaned_premier_data/all_cleaned.csv', 'w+')
#exportFile = ''
####################################################

path =r'../Premier_Data' # use your path
allFiles = glob.glob(path + "/*.csv")
#print (allFiles)
#frame = pd.DataFrame()
#list_ = []
#for file_ in allFiles:
#    df = pd.read_csv(file_,index_col=None, header=0)
#    list_.append(df)
#frame = pd.concat(list_)


######################################################

#reader = csv.reader(fileDir)

teamNo = 0
hRange = range(0,56)

for currFile in allFiles:
	print(currFile)
	fileDir = open(currFile,'rU')
	reader = csv.reader(fileDir)#,index_col=None)#, header=0)
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
				print (cdoc)
				search_term = cdoc[1]
				#print (search_term)
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

#fileDir.close()
exportFile.close()