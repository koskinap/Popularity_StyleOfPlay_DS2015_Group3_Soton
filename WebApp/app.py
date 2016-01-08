import json
import re

from flask import Flask
from flask import render_template

import os
from os import listdir
from os.path import isfile

import logging

#app = Flask(__name__)

app = Flask(__name__, static_url_path = "", static_folder = "static")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/popularity/<string:team>/<string:date>")
def matchpopularity(team, date):

	json_docs = []

	print(" ########################## "+team+"  ######## "+date)

	teamFiles = [f for f in listdir('.') if (isfile(f) and team in re.split('_', f) and date in re.split('_', f))]

	#directory = os.path.join(os.path.dirname(__file__), '../Tweets/TweetsFiles')
	#directory = os.path.join(os.path.dirname(__file__), '/Tweets/TweetsFiles')
	
	#APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
	#APP_STATIC = os.path.join(APP_ROOT, 'static')

	#directory = os.path.join(APP_STATIC, 'Tweets/TweetsFiles/')
	#print(directory)

	#teamFiles = [f for f in listdir(directory) if (isfile(f) and team in re.split('_', f) and date in re.split('_', f))]
	


	#logging.info(teamFiles[0])
	teamFile = teamFiles[0]

	countPos = 0
	countNeg = 0

	with open(teamFile,'r') as fi:
		for line in fi:
			jsonLine = json.loads(line)
			if jsonLine['team'] == team :
				if jsonLine['sentiment'] == "POS" :
					countPos += 1
				if jsonLine['sentiment'] == "NEG" :
					countNeg += 1

	entryPos = {}
	entryPos["label"] = "Positive"
	entryPos["count"] = countPos	
	json_docs.append(entryPos)

	entryNeg = {}
	entryNeg["label"] = "Negative"
	entryNeg["count"] = countNeg	
	json_docs.append(entryNeg)

	json_docs = json.dumps(json_docs)

	return json_docs


@app.route("/popularity")
@app.route("/popularity/<string:team>")
def gdata(team):

	json_docs = []

	print(" ########################## "+team)

	teamFiles = [f for f in listdir('.') if (isfile(f) and team in re.split('_', f))]

	for teamFile in teamFiles :
			
		matchDate = re.split('_', teamFile)[0]
		countPos = 0
		countNeg = 0

		with open(teamFile,'r') as fi:
			for line in fi:
				jsonLine = json.loads(line)
				if jsonLine['team'] == team :
					if jsonLine['sentiment'] == "POS" :
						countPos += 1
					if jsonLine['sentiment'] == "NEG" :
						countNeg += 1

		entry = {}
		entry["date"] = matchDate
		entry["pos_count"] = countPos
		entry["neg_count"] = countNeg	
		json_docs.append(entry)

	newlist = sorted(json_docs, key=lambda k: k['date'])

	json_docs = json.dumps(newlist)

	return json_docs

@app.route("/stats/<string:feature>/<string:team>")
def teamFeature(team,feature):

	teamsDic = {"ARSENAL":"1","ASTONVILLA":"2","BOURNEMOUTH":"3","CHELSEA":"4","CRYSTALPALACE":"5","EVERTON":"6","LEICESTER":"7","LIVERPOOL":"8",
		"MANCITY":"9","MANUNITED":"10","NEWCASTLE":"11","NORWICH":"12","SOUTHAMPTON":"13","STOKE":"14","SUNDERLAND":"15","SWANSEA":"16",
		"TOTENHAM":"17","WATFORD":"18","WESTBROM":"19","WESTHAM":"20"}

	json_docs = []

	dates = [re.split('_', f)[0] for f in listdir('.') if (isfile(f) and team in re.split('_', f))]
	
	featuresFile = 'classified_data.json'

	datesWithNoStats = dates # Has all the dates having tweets at first, a date that has stats will be remove from it

	with open(featuresFile) as data_file:
		data = json.load(data_file)

		for stat in data:

			statDate = stat['matchDate']

			teamNo = teamsDic[team]

#			if (stat['team'] == team and statDate in dates):
			if (stat['teamNo'] == teamNo and statDate in dates):
				feat = {}
				feat["value"] = stat[feature]
				feat["date"] = statDate
				json_docs.append(feat)
				datesWithNoStats.remove(statDate)

		for date in datesWithNoStats :
			feat = {}
			feat["value"] = "0"
			feat["date"] = date
			json_docs.append(feat)
				
	orderedDocs = sorted(json_docs, key=lambda k: k['date'])
	json_docs = json.dumps(orderedDocs)

	return json_docs



@app.route("/stats_details/<string:team>/<string:date>")
def stats(team, date):

	teamsDic = {"ARSENAL":"1","ASTONVILLA":"2","BOURNEMOUTH":"3","CHELSEA":"4","CRYSTALPALACE":"5","EVERTON":"6","LEICESTER":"7","LIVERPOOL":"8",
		"MANCITY":"9","MANUNITED":"10","NEWCASTLE":"11","NORWICH":"12","SOUTHAMPTON":"13","STOKE":"14","SUNDERLAND":"15","SWANSEA":"16",
		"TOTENHAM":"17","WATFORD":"18","WESTBROM":"19","WESTHAM":"20"}
		
	json_docs = []

	teamsDic = {"ARSENAL":"1","ASTONVILLA":"2","BOURNEMOUTH":"3","CHELSEA":"4","CRYSTALPALACE":"5","EVERTON":"6","LEICESTER":"7","LIVERPOOL":"8",
		"MANCITY":"9","MANUNITED":"10","NEWCASTLE":"11","NORWICH":"12","SOUTHAMPTON":"13","STOKE":"14","SUNDERLAND":"15","SWANSEA":"16",
		"TOTENHAM":"17","WATFORD":"18","WESTBROM":"19","WESTHAM":"20"}

	with open('stats.json') as data_file:
		data = json.load(data_file)

		for stat in data:

			statDate = stat['matchDate']
			dateParts = re.split('/', statDate)
			formattedDate = dateParts[2].replace(' ','')+"-"+dateParts[1]+"-"+dateParts[0]

			teamNo = teamsDic[team]

#			if (stat['team'] == team and statDate in dates):
#			if (stat['team'] == team and formattedDate == date):
			if (stat['teamNo'] == teamNo and formattedDate == date):
				_stat = {}
				_stat["passes"] = stat['passes']
				_stat["shotsOnTarget"] = stat['shotsOnTarget']
				_stat["shotsOffTarget"] = stat['shotsOffTarget']
				_stat["corners"] = stat['corners']
				_stat["foulsConceded"] = stat['foulsConceded']
				_stat["goals"] = stat['goals']
				_stat["foulsWon"] = stat['foulsWon']
				_stat["possesion"] = stat['possesion']
				_stat["offSide"] = stat['offSide']
				_stat["yellowCards"] = stat['yellowCards']
				json_docs.append(_stat)
				break


	json_docs = json.dumps(json_docs)

	return json_docs


@app.route("/2/")
def index2():
	return render_template("index2.html")


@app.route("/data/<string:team>/<string:feature>")
def data(team,feature):

		json_docs = []

		teamsDic = {"ARSENAL":"1","ASTONVILLA":"2","BOURNEMOUTH":"3","CHELSEA":"4","CRYSTALPALACE":"5","EVERTON":"6","LEICESTER":"7","LIVERPOOL":"8",
				"MANCITY":"9","MANUNITED":"10","NEWCASTLE":"11","NORWICH":"12","SOUTHAMPTON":"13","STOKE":"14","SUNDERLAND":"15","SWANSEA":"16",
				"TOTENHAM":"17","WATFORD":"18","WESTBROM":"19","WESTHAM":"20"}

		sourceFile = open('../cleaned_premier_data/classified_data.json')

		teamIndex = teamsDic[team]


		with sourceFile as f:
			data = json.load(f)

			for doc in data:
				
				if doc["teamNo"] == teamIndex:
					feat = {}
					feat["value1"] = doc[feature]
					feat["value2"] = doc["googleTrendsIndex"]

					json_docs.append(feat) 
		# feat = {}
		# feat["value1"] = team
		# feat["value2"] = feature
		# json_docs.append(feat)
				
		# feat2 = {}
		# feat2["value1"] = team
		# feat2["value2"] = feature
		# json_docs.append(feat2)

		# feat3 = {}
		# feat3["value1"] = team
		# feat3["value2"] = feature
		# json_docs.append(feat3)
						
		json_docs = json.dumps(json_docs)

		return json_docs

@app.route("/3/")
def index3():
	return render_template("index3.html")



@app.route("/interest_features/<string:interest>")
def interest_features(interest):

	json_docs = []

	sourceFile = open('../cleaned_premier_data/classified_data.json')
	with sourceFile as f:
		data = json.load(f)
		for doc in data:

			idx = doc["googleTrendsIndex"]
			if((interest == "HIGH" and idx > 66) or (interest == "MED" and idx in range(34,67)) or (interest == "LOW" and idx < 34) ):
				feat1 = {}
				feat1["value1"] = "Accuracy"
				feat1["value2"] = doc["Accuracy"]
				json_docs.append(feat1)

				feat2 = {}
				feat2["value1"] = "Aggressiveness"
				feat2["value2"] = doc["Aggressiveness"]
				json_docs.append(feat2)
				
				feat3 = {}
				feat3["value1"] = "Attack"
				feat3["value2"] = doc["Attack"]
				json_docs.append(feat3)

				feat4 = {}
				feat4["value1"] = "Teamplay"
				feat4["value2"] = doc["Teamplay"]
				json_docs.append(feat4)

				feat5 = {}
				feat5["value1"] = "Pressure"
				feat5["value2"] = doc["Pressure"]
				json_docs.append(feat5)	
			

					
	json_docs = json.dumps(json_docs)

	return json_docs


@app.route("/data_allteams/<string:feature>")
def data_allteams(feature):

				json_docs = []



				sourceFile = open('../cleaned_premier_data/classified_data.json')


				with sourceFile as f:
					data = json.load(f)

					for doc in data:
						
						feat = {}
						feat["value1"] = doc[feature]
						feat["value2"] = doc["googleTrendsIndex"]
						feat["teamNo"] = doc["teamNo"]
						feat["teamName"] = doc["team"]

						json_docs.append(feat)
						
				# feat = {}
				# feat["value1"] = team
				# feat["value2"] = feature
				# json_docs.append(feat)
						
				# feat2 = {}
				# feat2["value1"] = team
				# feat2["value2"] = feature
				# json_docs.append(feat2)

				# feat3 = {}
				# feat3["value1"] = team
				# feat3["value2"] = feature
				# json_docs.append(feat3)
								
				json_docs = json.dumps(json_docs)

				return json_docs		
		
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
