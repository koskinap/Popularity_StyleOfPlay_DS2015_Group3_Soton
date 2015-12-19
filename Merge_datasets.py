#Merge popularity with match statistics
import os.path
import csv
import sys
import json
import datetime
#import time

statsFile = open('../cleaned_premier_data/cleaned_stats.json', 'r')
gtrendsFile = open('../cleaned_premier_data/all_cleaned2.csv', 'wb+')
tempFile = open('../cleaned_premier_data/merged_data.csv', 'wb+')
destFile = open('../cleaned_premier_data/final_dataset.csv', 'wb+')

f = csv.writer(tempFile)
f.writerow(["matchDate", "matchId", "team", "teamNo", "passes", "shotsOnTarget", "shotsOffTarget", "corners", "foulsConceded", "accuratePasses", "goals", "foulsWon", "possession", "offSide", "yellowCards"])

#Convert Json to CSV file
data = json.load(statsFile)
for cdoc in data:
	#Convert date
	temp = datetime.datetime.strptime(str(cdoc["matchDate"]), '%d/%m/%Y ').strftime('%Y-%m-%d')
	f.writerow([temp,cdoc["matchId"], cdoc["team"], cdoc["teamNo"], cdoc["passes"], cdoc["shotsOnTarget"], cdoc["shotsOffTarget"], cdoc["corners"], cdoc["foulsConceded"], cdoc["accuratePasses"], cdoc["goals"], cdoc["foulsWon"], cdoc["possesion"], cdoc["offSide"], cdoc["yellowCards"] ])	
