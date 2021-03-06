import time
import json
import tweepy
import nltk
import re
import random

from datetime import datetime


api = None

word_features = {}
word_featuresSent = []

def getClassifier(team):
	if team == 'ARSENAL':
		return arsenalClassifier
	if team == 'LEICESTER':
		return leicesterClassifier
	if team == 'MANCITY':
		return manCityClassifier
	if team == 'MANUNITED':
		return manUnitedClassifier
	if team == 'TOTENHAM':
		return totenhamClassifier
	if team == 'CRYSTALPALACE':
		return crystalPalaceClassifier
	if team == 'WATFORD':
		return watfordClassifier
	if team == 'WESTHAM':
		return westHamClassifier
	if team == 'LIVERPOOL':
		return liverpoolClassifier
	if team == 'EVERTON':
		return evertonClassifier
	if team == 'STOKE':
		return stokeClassifier
	if team == 'SOUTHAMPTON':
		return southamptonClassifier
	if team == 'WESTBROM':
		return westBromClassifier
	if team == 'BOURNEMOUTH':
		return bournemouthClassifier
	if team == 'CHELSEA':
		return chelseaClassifier
	if team == 'NEWCASTLE':
		return newCastleClassifier
	if team == 'NORWICH':
		return norwichClassifier
	if team == 'SWANSEA':
		return swanseaClassifier
	if team == 'SUNDERLAND':
		return sunderlandClassifier
	if team == 'ASTONVILLA':
		return astonVillaClassifier


def getClassifierKey(team):
	return team



def login():

	ACCESS_TOKEN = '1681062247-YXE4HfZCwLWBhE7SvNL2TmNC2vwHsBFH6Zvtjyb'
	ACCESS_SECRET = 'b9cjJxoO8ZwnUTIvnySk8VoZklm3MQpsU3jqEqlTBhOP3'
	CONSUMER_KEY = 'VCwBAlUbXs8uCLkpHTOLYiOCl'
	CONSUMER_SECRET = '4R06f1I5K1Vmj9b5i4IbrB3xifrD96IIHSxactyMypT3w9ce7k'

	auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	api = tweepy.API(auth, wait_on_rate_limit=True,
					   wait_on_rate_limit_notify=True)
	return api


def analyzeMatchTweets(match):
	matchDay = datetime.strptime(match["startDate"], '%Y-%m-%d')
	matchStartTime = match["startTime"] 
	startCollectTime = datetime.strptime(match["startDate"]+" "+matchStartTime, '%Y-%m-%d %H:%M')
	endCollectTime = datetime.strptime(match["endCollectTime"], '%Y-%m-%d %H:%M')
	endCollectDay = match["endCollectTime"].split()[0]

	team1 = match["teams"][0]["team"]
	team2 = match["teams"][1]["team"]
	hashtag1 = match["hashtags"][0]["hashtag"]
	hashtag2 = match["hashtags"][1]["hashtag"]

	fileName = match["startDate"]+"_"+team1+"_"+team2

	classifier1 = getClassifier(team1)
	classifier2 = getClassifier(team2)

	searchQuery = hashtag1+" OR "+hashtag2

	print(" ##################### Search Query : "+searchQuery)
	max_id = -1
	with open(fileName, 'a') as f:
		
		count = 0
		matchStartTimeReached = False
		while 1 == 1 :
			try:
				if (max_id <= 0):
					new_tweets = api.search(q=searchQuery, count=50)
				else:
					new_tweets = api.search(q=searchQuery, count=50, max_id=str(max_id - 1))
				if not new_tweets:
					print("No more tweets found")
					break

			except (Exception) as e:
				new_tweets = []
				print(" ###################### Exception Catched ")

			
			for tweet in new_tweets :
				print("New Tweet   "+tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"))
				if tweet.created_at < startCollectTime :
					matchStartTimeReached = True
					break
				if tweet.created_at < endCollectTime :
					count += 1
					print(" *** Saving ......... ")

					# Start Analyzing

					tweetToAnalyze = tweet.text

					# prepare tweet for classification
					tweetWords = re.sub("[^\w]", " ",  tweetToAnalyze).split()
					lowerTweetWords = []
					[lowerTweetWords.append(word.lower()) for word in tweetWords]
		
					#classify tweet 
					isTeam1 = ( classifier1.classify(findFeatures(lowerTweetWords,getClassifierKey(team1))) != 'no')
					isTeam2 = ( classifier2.classify(findFeatures(lowerTweetWords,getClassifierKey(team2))) != 'no')
		
					if isTeam1 and isTeam2:
						print(" Classified as relevant to Both Teams. Ignoring !!!!!!!")
					elif isTeam1 or isTeam2:
						# sentimentAnalysis
						dist = sentimentClassifier.prob_classify(findFeaturesSentiment(lowerTweetWords))
						sentiment = dist.max()
						prob = dist.prob(sentiment)

						if isTeam1 and (prob > 0.65):

							_sentiment1 = {}
							_sentiment1['tweet_id'] = tweet.id
							_sentiment1['tweet'] = tweetToAnalyze
							_sentiment1['created_at'] = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
							_sentiment1['coordinates'] = tweet.coordinates
							_sentiment1['geo'] = tweet.geo
							_sentiment1['team'] = team1
							_sentiment1['prob'] = prob
							if tweet.place is None:
								_sentiment1['country'] = None
							else:
								_sentiment1['country'] = tweet.place.country
							_sentiment1['sentiment'] = sentiment
							json_sentiment1 = json.dumps(_sentiment1)
							f.write(json_sentiment1+'\n')

						if isTeam2 and (prob > 0.65):
							_sentiment2 = {}
							_sentiment2['tweet_id'] = tweet.id
							_sentiment2['tweet'] = tweetToAnalyze
							_sentiment2['created_at'] = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
							_sentiment2['coordinates'] = tweet.coordinates
							_sentiment2['geo'] = tweet.geo
							_sentiment2['team'] = team2
							_sentiment2['prob'] = prob
							if tweet.place is None:
								_sentiment2['country'] = None
							else:
								_sentiment2['country'] = tweet.place.country
							_sentiment2['sentiment'] = sentiment
							json_sentiment2 = json.dumps(_sentiment2)
							f.write(json_sentiment2+'\n')


					# End Analyzing
			if new_tweets:
				max_id = new_tweets[-1].id

			if matchStartTimeReached :
				break


def findFeatures(tweet,classifierKey):
	words = set(tweet)
	features = {}

	global word_features

	for w in word_features[classifierKey]:
		features[w] = (w in words)
	return features

def findFeaturesSentiment(tweet):
	wordsSent = set(tweet)
	featuresSent = {}

	global word_featuresSent

	for w in word_featuresSent:
		featuresSent[w] = (w in wordsSent)
	return featuresSent

def prepareClassifier(trainingFile,classifierKey):
	
	tweets = []

	with open(trainingFile) as training:
		tweetsFile = json.load(training)
		for tweet in tweetsFile["tweets"]:
			text = tweet["tweet"]
			category = tweet["category"]
			wordList = re.sub("[^\w]", " ",  text).split()
			lowerWordList = []
			[lowerWordList.append(word.lower()) for word in wordList]
			tweets.append((lowerWordList,category))

	random.shuffle(tweets)

	all_words = []

	with open(trainingFile) as training:
		tweetsFile = json.load(training)
		for tweet in tweetsFile["tweets"]:
			text = tweet["tweet"]
			wordList = re.sub("[^\w]", " ",  text).split()
			for w in wordList:
				all_words.append(w.lower())

	all_words = nltk.FreqDist(all_words)

	# just the keys
	global word_features
	word_features[classifierKey] = list(all_words.keys())


	# convert the training set to a list of tuples ( [featuresPresence] , category)
	featuresInTweets = []
	for (tweet, category) in tweets:
		featuresInTweets.append((findFeatures(tweet,classifierKey),category))

	trainingSet = featuresInTweets
	classifier = nltk.NaiveBayesClassifier.train(trainingSet)
	
	return classifier


def prepareSentimentClassifier():
	
	tweets = []
	
	with open('trainingSetSentiments.json') as training:
		tweetsFile = json.load(training)
		for tweet in tweetsFile["tweets"]:
			text = tweet["tweet"]
			category = tweet["category"]
			wordList = re.sub("[^\w]", " ",  text).split()
			lowerWordList = []
			[lowerWordList.append(word.lower()) for word in wordList]
			tweets.append((lowerWordList,category))

	random.shuffle(tweets)

	all_words = []

	with open('trainingSetSentiments.json') as training:
		tweetsFile = json.load(training)
		for tweet in tweetsFile["tweets"]:
			text = tweet["tweet"]
			wordList = re.sub("[^\w]", " ",  text).split()
			for w in wordList:
				all_words.append(w.lower())

	all_words = nltk.FreqDist(all_words)

	# just the keys
	global word_featuresSent
	word_featuresSent = list(all_words.keys())


	# convert the training set to a list of tuples ( [featuresPresence] , category)
	featuresInTweets = []
	for (tweet, category) in tweets:
		featuresInTweets.append((findFeaturesSentiment(tweet),category))

	trainingSet = featuresInTweets
	sentimentClassifier = nltk.NaiveBayesClassifier.train(trainingSet)

	return sentimentClassifier

try:

############################## Prepare Classifiers ##############################

	arsenalClassifier = prepareClassifier('trainingSetArsenal.json',"ARSENAL")
	leicesterClassifier = prepareClassifier('trainingSetLeicester.json',"LEICESTER")
	manCityClassifier = prepareClassifier('trainingSetManCity.json',"MANCITY")
	manUnitedClassifier = prepareClassifier('trainingSetManUnited.json',"MANUNITED")
	totenhamClassifier = prepareClassifier('trainingSetTotenham.json',"TOTENHAM")
	crystalPalaceClassifier = prepareClassifier('trainingSetCrystalPalace.json',"CRYSTALPALACE")
	watfordClassifier = prepareClassifier('trainingSetWatford.json',"WATFORD")
	westHamClassifier = prepareClassifier('trainingSetWestHam.json',"WESTHAM")
	liverpoolClassifier = prepareClassifier('trainingSetLiverpool.json',"LIVERPOOL")
	evertonClassifier = prepareClassifier('trainingSetEverton.json',"EVERTON")
	stokeClassifier = prepareClassifier('trainingSetStoke.json',"STOKE")
	southamptonClassifier = prepareClassifier('trainingSetSouthampton.json',"SOUTHAMPTON")
	westBromClassifier = prepareClassifier('trainingSetWestBrom.json',"WESTBROM")
	bournemouthClassifier = prepareClassifier('trainingSetBournemouth.json',"BOURNEMOUTH")
	chelseaClassifier = prepareClassifier('trainingSetChelsea.json',"CHELSEA")
	newCastleClassifier = prepareClassifier('trainingSetNewCastle.json',"NEWCASTLE")
	norwichClassifier = prepareClassifier('trainingSetNorwich.json',"NORWICH")
	swanseaClassifier = prepareClassifier('trainingSetSwansea.json',"SWANSEA")
	sunderlandClassifier = prepareClassifier('trainingSetSunderland.json',"SUNDERLAND")
	astonVillaClassifier = prepareClassifier('trainingSetAstonVilla.json',"ASTONVILLA")

	sentimentClassifier = prepareSentimentClassifier()

###################################################################################	


	ACCESS_TOKEN = '1681062247-YXE4HfZCwLWBhE7SvNL2TmNC2vwHsBFH6Zvtjyb'
	ACCESS_SECRET = 'b9cjJxoO8ZwnUTIvnySk8VoZklm3MQpsU3jqEqlTBhOP3'
	CONSUMER_KEY = 'VCwBAlUbXs8uCLkpHTOLYiOCl'
	CONSUMER_SECRET = '4R06f1I5K1Vmj9b5i4IbrB3xifrD96IIHSxactyMypT3w9ce7k'

	auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


	# get today's file
	with open('matches.json') as data_file:
		data = json.load(data_file)

		for match in data["matches"]:

			analyzeMatchTweets(match, )


	print("END")

except Exception as e:
	print(type(e))
	print(e.args)
	print(e)

