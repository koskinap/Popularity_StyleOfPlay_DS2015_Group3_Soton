#Parse stats from json file
import os.path
import sys
import glob
import json

statsFile = open('../Premier_Data/stats.json')

teamsDic = {"Arsenal":"1","A Villa":"2","B'mouth":"3","Chelsea":"4","C Palace":"5","Everton":"6","Leicester":"7","Liverpool":"8",
			"Man City":"9","Man Utd":"10","Newcastle":"11","Norwich":"12","So'ton":"13","Stoke":"14","S'land":"15","Swansea":"16",
			"Tottenham":"17","Watford":"18","W Brom":"19","West Ham":"20"}

output = []
badOutput = []
keys = [ "matchDate", "matchId", "team", "teamNo", "passes", "shotsOnTarget", "shotsOffTarget", "corners", "foulsConceded", "accuratePasses", "goals", "foulsWon", "possesion", "offSide", "yellowCards" ]

with statsFile as data_file:
	data = json.load(data_file)
	print len(data)
	for cdoc in data:
		i = cdoc['team'].strip()
		#probably some team names do not match exactly the names of th dictionary
		# if i in teamsDic:
		cdoc['teamNo'] = teamsDic[i]
		if len(cdoc) < 15:
				#badOutput.append(cdoc)
			for k in keys:
				cdoc.setdefault(k, "0")
		output.append(cdoc)

with open('../cleaned_premier_data/cleaned_stats.json', mode = 'w') as f:
 	json.dump(output, f, indent = 2)

# with open('../cleaned_premier_data/badformat_stats.json', mode = 'w') as g:
# 	json.dump(badOutput, g, indent = 2)

