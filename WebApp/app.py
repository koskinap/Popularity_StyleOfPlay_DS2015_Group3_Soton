import json
import re

from flask import Flask
from flask import render_template

from os import listdir
from os.path import isfile


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
			if (stat['team'] == team and formattedDate == date):
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


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
