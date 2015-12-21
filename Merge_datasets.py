#Merge popularity with match statistics
import os.path
import csv
import sys
import json
import datetime
#import time

statsFile = open('../cleaned_premier_data/cleaned_stats.json', 'r')
gtrendsFile = open('../cleaned_premier_data/cleaned_gtrends.csv', 'r')
tempFile = open('../cleaned_premier_data/merged_data.csv', 'wb+')
destFile = open('../cleaned_premier_data/final_dataset.csv', 'wb+')

f = csv.writer(tempFile)
cNames = ["matchDate", "matchId", "team", "teamNo", "passes", "shotsOnTarget", "shotsOffTarget", "corners", "foulsConceded", 
			"accuratePasses", "goals", "foulsWon", "possession", "offSide", "yellowCards", "popularity"]
f.writerow(cNames)
gReader = csv.reader(gtrendsFile)

#Convert Json to CSV file
data = json.load(statsFile)

for cdoc in data:
	#Convert date
	mDate = datetime.datetime.strptime(str(cdoc["matchDate"]), '%d/%m/%Y ').strftime('%Y-%m-%d')
	for pdoc in gReader:
		# if pdoc[3] == cdoc["teamNo"] and (datetime.datetime.strptime(mDate, '%Y-%m-%d') >= datetime.datetime.strptime(pdoc[1], '%Y-%m-%d')) and (datetime.datetime.strptime(mDate, '%Y-%m-%d') <= datetime.datetime.strptime(pdoc[2], '%Y-%m-%d')):
		# 	temp = pdoc[4]

	f.writerow([mDate,cdoc["matchId"], cdoc["team"], cdoc["teamNo"], cdoc["passes"], cdoc["shotsOnTarget"], cdoc["shotsOffTarget"], cdoc["corners"], cdoc["foulsConceded"], cdoc["accuratePasses"], cdoc["goals"], cdoc["foulsWon"], cdoc["possesion"], cdoc["offSide"], cdoc["yellowCards"],"0"])	

fReader = csv.reader(tempFile)

for i in fReader:
	for j in gReader:
		if i[3] == j[3] and (datetime.datetime.strptime(i[1], '%Y-%m-%d') >= datetime.datetime.strptime(pdoc[1], '%Y-%m-%d')) and (datetime.datetime.strptime(mDate, '%Y-%m-%d') <= datetime.datetime.strptime(pdoc[2], '%Y-%m-%d')):
		 	temp = pdoc[4]