import json

from flask import Flask
from flask import render_template

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")



@app.route("/popularity")
@app.route("/popularity/<string:team>")
def gdata(team):

	json_docs = []

	print(" ########################## "+team)

	if team == "MANUNITED" :

		doc1 = {}
		doc1["date"] = "12/12"
		doc1["pos_count"] = 90
		doc1["neg_count"] = 20	
		json_docs.append(doc1)

		doc2 = {}
		doc2["date"] = "12/19"
		doc2["pos_count"] = 20
		doc2["neg_count"] = 70	
		json_docs.append(doc2)

	if team == "NORWICH" :

		doc1 = {}
		doc1["date"] = "12/12"
		doc1["pos_count"] = 50
		doc1["neg_count"] = 25	
		json_docs.append(doc1)

		doc2 = {}
		doc2["date"] = "12/19"
		doc2["pos_count"] = 30
		doc2["neg_count"] = 20	
		json_docs.append(doc2)

	json_docs = json.dumps(json_docs)

	return json_docs


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
