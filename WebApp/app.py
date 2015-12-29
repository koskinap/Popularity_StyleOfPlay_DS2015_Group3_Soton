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

	json_docs = json.dumps(json_docs)

	return json_docs

@app.route("/stats/possesion/<string:team>")
def teamPossession(team):

	json_docs = []

	dates = [re.split('_', f)[0] for f in listdir('.') if (isfile(f) and team in re.split('_', f))]
	
	with open('stats.json') as data_file:
		data = json.load(data_file)

		for stat in data:

			statDate = stat['matchDate']
			dateParts = re.split('/', statDate)
			formattedDate = dateParts[2].replace(' ','')+"-"+dateParts[1]+"-"+dateParts[0]
			print(formattedDate)
			if (stat['team'] == team and formattedDate in dates):
				value = stat['possesion']
				level = getPossessionLevel(float(value))
				possession = {}
				possession["value"] = level
				json_docs.append(possession)

	json_docs = json.dumps(json_docs)

	return json_docs

@app.route("/test/<string:team>/<string:date>")
def test(team, date):
		
	json_docs = []

	with open('stats.json') as data_file:
		data = json.load(data_file)

		for stat in data:

			statDate = stat['matchDate']
			dateParts = re.split('/', statDate)
			formattedDate = dateParts[2].replace(' ','')+"-"+dateParts[1]+"-"+dateParts[0]

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

def getPossessionLevel(value):

	if value < 35 :
		return 0
	if 35 < value < 60 :
		return 1
	if value > 60 :
		return 2 


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
