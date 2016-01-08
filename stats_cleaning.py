#Parse stats from json file
import os.path
import sys
import glob
import json

statsFile = open('Premier_Data/stats.json')

# Dictionary with key values equal to team names as they appear in statistics json file and keys equal to a unique numeric value that characterises a team
teamsDic = {"Arsenal":"1","A Villa":"2","B'mouth":"3","Chelsea":"4","C Palace":"5","Everton":"6","Leicester":"7","Liverpool":"8",
			"Man City":"9","Man Utd":"10","Newcastle":"11","Norwich":"12","So'ton":"13","Stoke":"14","S'land":"15","Swansea":"16",
			"Tottenham":"17","Watford":"18","W Brom":"19","West Ham":"20"}

output = []
badOutput = []
keys = [ "matchDate", "matchId", "team", "teamNo", "passes", "shotsOnTarget", "shotsOffTarget", "corners", "foulsConceded", "accuratePasses", "goals", "foulsWon", "possesion", "offSide", "yellowCards" ]

with statsFile as data_file:
	data = json.load(data_file)

	for cdoc in data:
		# clean team names from spaces
		i = cdoc['team'].strip()
		cdoc['teamNo'] = teamsDic[i]
		# if the doc does not match the format with 15 keys,return it in a file with bad formmated stats data
		if len(cdoc) < 15:
			badOutput.append(cdoc)
			# if a key does not appear in current document,add this key with default value 0
			for k in keys:
				cdoc.setdefault(k, "0")
		output.append(cdoc)

with open('cleaned_premier_data/cleaned_stats.json', mode = 'w') as f:
 	json.dump(output, f, indent = 2)

with open('cleaned_premier_data/badformat_stats.json', mode = 'w') as g:
	json.dump(badOutput, g, indent = 2)

