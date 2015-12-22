import json
import re

from flask import Flask
from flask import render_template

from os import listdir
from os.path import isfile



app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")



@app.route("/popularity")
@app.route("/popularity/<string:team>")
def gdata(team):

	json_docs = []

	print(" ########################## "+team)

#	if team == "MANUNITED" :

	teamFiles = [f for f in listdir('.') if (isfile(f) and team in re.split('_', f))]

	for teamFile in teamFiles :
			
		matchDate = re.split('_', teamFile)[0]
		countPos = 0
		countNeg = 0

		with open(teamFile,'r') as fi:
			for line in fi:
				jsonLine = json.loads(line)
				if jsonLine['team'] == team :
					if jsonLine['sentiment'] == "pos" :
						countPos += 1
					if jsonLine['sentiment'] == "neg" :
						countNeg += 1

		entry = {}
		entry["date"] = matchDate
		entry["pos_count"] = countPos
		entry["neg_count"] = countNeg	
		json_docs.append(entry)


#	if team == "NORWICH" :

#		doc1 = {}
#		doc1["date"] = "12/12"
#		doc1["pos_count"] = 50
#		doc1["neg_count"] = 25	
#		json_docs.append(doc1)

#		doc2 = {}
#		doc2["date"] = "12/19"
#		doc2["pos_count"] = 30
#		doc2["neg_count"] = 20	
#		json_docs.append(doc2)

	json_docs = json.dumps(json_docs)

	return json_docs


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
