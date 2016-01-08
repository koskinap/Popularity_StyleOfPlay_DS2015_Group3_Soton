#Merge popularity with match statistics
import os.path
import csv
import sys
import json
import datetime

statsFile = open('cleaned_premier_data/cleaned_stats.json', 'r')
gtrendsFile = open('cleaned_premier_data/cleaned_gtrends.csv', 'rU')
mergeFile = open('cleaned_premier_data/merged_data.csv', 'wb+')

f = csv.writer(mergeFile)
cNames = ["matchDate", "matchId", "team", "teamNo", "passes", "shotsOnTarget", "shotsOffTarget", "corners", "foulsConceded", 
			"accuratePasses", "goals", "foulsWon", "possession", "offSide", "yellowCards", "googleTrendsIndex"]
f.writerow(cNames)

gReader = csv.reader(gtrendsFile)

#Convert Json to CSV file
data = json.load(statsFile)

output = []
for cdoc in data:
	#Convert date into same format as Google trends dataset
	mDate = datetime.datetime.strptime(str(cdoc["matchDate"]), '%d/%m/%Y ').strftime('%Y-%m-%d')
	cdoc['matchDate'] = mDate
	output.append(cdoc)

#print len(output)
for i in gReader:
	for j in output:
		# match Google Trends index with match statistics using teamNo and date as keys(date fits within a week)
		if i[3] == str(j["teamNo"]) and (datetime.datetime.strptime(j["matchDate"], '%Y-%m-%d') >= datetime.datetime.strptime(i[1], '%Y-%m-%d')) and (datetime.datetime.strptime(j["matchDate"], '%Y-%m-%d') <= datetime.datetime.strptime(i[2], '%Y-%m-%d')):
			f.writerow([j["matchDate"],j["matchId"], j["team"], j["teamNo"], j["passes"], j["shotsOnTarget"], j["shotsOffTarget"], j["corners"], j["foulsConceded"], j["accuratePasses"], j["goals"], j["foulsWon"], j["possesion"], j["offSide"], j["yellowCards"],i[4]])

reader = csv.reader(open('cleaned_premier_data/merged_data.csv', 'rU'))
