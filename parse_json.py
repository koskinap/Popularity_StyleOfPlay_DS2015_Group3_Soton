#Parse stats from json file
import os.path
import csv
import sys
import glob
import json
from pprint import pprint

statsFile = open('../Premier_Data/stats.json')


# teamsDic = {"Arsenal":1,"A Villa":2,"B'mouth":3,"Chelsea":4,"C Palace":5,"Everton":6,"Leicester":7,"Liverpool":8,"Man City":9,"Man Utd":10,
# 			"Newcastle":11,"Norwich":12,"So'ton":13,"Stoke":14,"S'land":15,"Swansea":16,"Tottenham":17,"Watford":18,"W Brom":19,"West Ham":20}
# teamsDic = sorted({"1":"Arsenal","2":"A Villa","3":"B'mouth","4":"Chelsea","5":"C Palace","6":"Everton","7":"Leicester",
# 					"8":"Liverpool","9":"Man City","10":"Man Utd","11":"Newcastle","12":"Norwich","13":"So'ton","14":"Stoke",
# 					"15":"S'land","16":"Swansea","17":"Tottenham","18":"Watford","19":"W Brom","20":"West Ham"})
teamsDic = {"Arsenal":"1","A Villa":"2","B'mouth":"3","Chelsea":"4","C Palace":"5","Everton":"6","Leicester":"7","Liverpool":"8",
			"Man City":"9","Man Utd":"10","Newcastle":"11","Norwich":"12","So'ton":"13","Stoke":"14","S'land":"15","Swansea":"16",
			"Tottenham":"17","Watford":"18","W Brom":"19","West Ham":"20"}


output = []
with statsFile as data_file:    
	data = json.load(data_file)
	for cdoc in data:
		i = cdoc['team']
		if i in teamsDic:
			cdoc['teamNo'] = teamsDic[i]
			output.append(cdoc)

with open('../cleaned_premier_data/cleaned_stats.json', mode = 'w') as f:
 	json.dump(output,f,indent =2)