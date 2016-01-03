import os.path
import csv
import sys
import json
import datetime


inputFile = open('cleaned_premier_data/merged_data.csv', 'rU')
csvOutputFile  = open('cleaned_premier_data/classified_data.csv', 'wb+')
# Means and stds about stats coming from analysis in Matlab

means = [438.87, 4.34, 5.03, 5.28, 10.87, 78.02, 1.33, 10.52, 50, 1.99, 1.73]
stds = [104.53, 2.49, 2.56, 2.86, 3.72, 6.54, 1.21, 3.61, 10.47, 1.52, 1.20]

featMeans = [11.88,	5.99, 4.04, 2.09, 5.99]
featStds = [1.55, 1.51, 0.99, 1.01, 1.24]

temp_headers = ['passes', 'shotsOnTarget', 'shotsOffTarget', 'corners', 'foulsConceded', 
				'accuratePasses', 'goals', 'foulsWon', 'possession', 'offSide', 'yellowCards']

featureKeys = ['matchDate', 'matchId', 'team', 'teamNo', 'Attack' , 'Teamplay' , 'Aggressiveness' , 'Accuracy' , 'Pressure' , 'googleTrendsIndex']

attack = [1, 2, 3, 6, 7, 9]
attackFactors = [1, 1, 1, 1, 1, 1]

teamPlay = [0, 5, 8]
teamPlayFactors = [1, 1, 1]

aggressiveness = [4, 10]
aggressivenessFactors = [1, 1]

accuracy = [1 ,5 ,9]
accuracyFactors = [1, 1, -1]

pressure = [2, 3, 8]
pressureFactors = [1, 1, 1]

# defence = goalsConceded,foulsConceded,yellowcards

#efficiency ?????do we really need this? we have accuracy

output = []
with inputFile as infile, csvOutputFile as outFile:
	reader = csv.reader(inputFile)
	writer = csv.writer(outFile)
	
	# returns the headers or `None` if the input is empty
	headers = next(reader, None) 
	writer.writerow(featureKeys)


	for row in reader:
		static = list(row[j] for j in range(0,4))
		popIndex = row[15]

		content = list(row[i] for i in range(4,15))

		
		rates = []
 		for index,el in enumerate(content):

 			if (float(el) > means[index] + stds[index]):
 				rates.append(3)
 			elif( float(el) < means[index] - stds[index]):
 				rates.append(1)
 			else:
 				rates.append(2)

 		# At this point we have for each row in rates list the scale of each variable compared to mean +- standard deviation		
		#print(rates)
 		# After that comes the access of specific elements of the list for every feature of play
 		doc = {}
 		for i in range(0,4):
 			doc[featureKeys[i]] = static[i]
 		doc[featureKeys [len (featureKeys) - 1]] =  int(popIndex)

 		temp1 = 0
 		for index1,el1 in enumerate(attack):
 			temp1 += attackFactors[index1] * rates[el1]
 		doc[featureKeys[4]] = temp1

		temp2 = 0
 		for index2,el2 in enumerate(teamPlay):
 			temp2 += teamPlayFactors[index2] * rates[el2]
 		doc[featureKeys[5]] = temp2

 		temp3 = 0
 		for index3,el3 in enumerate(aggressiveness):
 			temp3 += aggressivenessFactors[index3] * rates[el3]
 		doc[featureKeys[6]] = temp3

 		temp4 = 0
 		for index4,el4 in enumerate(accuracy):
 			temp4 += accuracyFactors[index4] * rates[el4]
 		doc[featureKeys[7]] = temp4

 		temp5 = 0
 		for index5,el5 in enumerate(pressure):
 			temp5 += pressureFactors[index5] * rates[el5]
 		doc[featureKeys[8]] = temp5

 		output.append(doc)

 		csvList = static
 		for j in range(4,9):
 			level = 0
 			
 			if doc[featureKeys[j]] > featMeans[j-4] + featStds[j-4]*0.75 :
 				level = 3
 			elif doc[featureKeys[j]] < featMeans[j-4] -	 featStds[j-4]*0.75 :
 				level = 1
 			else:
 				level = 2

			csvList.append(level)
			doc[featureKeys[j]] = level

		#for 

 		csvList.append(popIndex)
 		writer.writerow(csvList)

with open('cleaned_premier_data/classified_data.json', mode = 'w') as f:
 	json.dump(output, f, indent = 2)



