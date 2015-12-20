import _thread
import time
import json
import tweepy
import nltk
import re
import random
from nltk.corpus import movie_reviews

word_features = {}
word_featuresSent = []

def getClassifier(team):
	if team == 'Man United':
		return manUnitedClassifier
	if team == 'Norwich City':
		return norwichClassifier
	return arsenalClassifier


def getClassifierKey(team):
	if team == 'Man United':
		return "MANUNITED"
	if team == 'Norwich City':
		return "NORWICH"


class Listener1(tweepy.StreamListener):

	endTime = 'a'
	team1 = 'team1'
	team2 = 'team2'

	def __init__(self, endTime, team1, team2):
		tweepy.StreamListener.__init__(self)
		self.endTime = endTime
		self.team1 = team1
		self.team2 = team2

	def on_status(self, status):
		
		tweetToAnalyze = status.text
		#print(tweetToAnalyze)
		print("New Tweet")
		#print(self.endTime)
		#print(self.team1)
		#print(self.team2)
		
		classifier1 = getClassifier(self.team1)
		classifier2 = getClassifier(self.team2)

		# prepare tweet for classification
		tweetWords = re.sub("[^\w]", " ",  tweetToAnalyze).split()
		lowerTweetWords = []
		#print(tweetWords)
		[lowerTweetWords.append(word.lower()) for word in tweetWords]
		
		#classify tweet 
		isTeam1 = ( classifier1.classify(findFeatures(lowerTweetWords,getClassifierKey(self.team1))) != 'no')
		isTeam2 = ( classifier2.classify(findFeatures(lowerTweetWords,getClassifierKey(self.team2))) != 'no')
		
		with open('sentiment', 'a') as f:

			if isTeam1 or isTeam2:
				# sentimentAnalysis
				sentiment = sentimentClassifier.classify(findFeaturesSentiment(lowerTweetWords))
				if isTeam1:
					# save tweetToAnalyze + team1 + date + sentiment
					#print(" ### ",tweetToAnalyze," ### Classified as ",self.team1, " ##### ",sentiment)
					_sentiment1 = {}
					_sentiment1['tweet'] = tweetToAnalyze
					#_sentiment['created_at'] = status.
					#_sentiment['coordinates'] = status.
					#_sentiment['geo'] = status.
					_sentiment1['team'] = self.team1
					#if status.place is None:
					#	_sentiment['country'] = None
					#else:
					#	_sentiment['country'] = status.place.country
					_sentiment1['sentiment'] = sentiment
					json_sentiment1 = json.dumps(_sentiment1)
					f.write(json_sentiment1+'\n')
				if isTeam2:
					# save tweetToAnalyze + team1 + date + sentiment
					#print(" ### ",tweetToAnalyze," ### Classified as ",self.team1, " ##### ",sentiment)
					_sentiment2 = {}
					_sentiment2['tweet'] = tweetToAnalyze
					#_sentiment['created_at'] = status.
					#_sentiment['coordinates'] = status.
					#_sentiment['geo'] = status.
					_sentiment2['team'] = self.team2
					#if status.place is None:
					#	_sentiment['country'] = None
					#else:
					#	_sentiment['country'] = status.place.country
					_sentiment2['sentiment'] = sentiment
					json_sentiment2 = json.dumps(_sentiment2)
					f.write(json_sentiment2+'\n')
		return True

pass

def login():

	ACCESS_TOKEN = '1681062247-YXE4HfZCwLWBhE7SvNL2TmNC2vwHsBFH6Zvtjyb'
	ACCESS_TOKEN_SECRET = 'b9cjJxoO8ZwnUTIvnySk8VoZklm3MQpsU3jqEqlTBhOP3'
	CONSUMER_KEY = 'VCwBAlUbXs8uCLkpHTOLYiOCl'
	CONSUMER_SECRET = '4R06f1I5K1Vmj9b5i4IbrB3xifrD96IIHSxactyMypT3w9ce7k'

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	return auth



def listenToStream(match):
	startTime = match["startTime"]
	#endTime = startTime + 24:00
	endTime = 'b'
	team1 = match["teams"][0]["team"]
	team2 = match["teams"][1]["team"]
	hashtag1 = match["hashtags"][0]["hashtag"]
	hashtag2 = match["hashtags"][1]["hashtag"]

	listener1 = Listener1(endTime,team1,team2)

	streaming1 = tweepy.streaming.Stream(auth, listener1, timeout=60)
	streaming1.filter(async=True, track=[hashtag1,hashtag2])
	# print(match)



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

	documents = [(list(movie_reviews.words(fileid)), category)
		for category in movie_reviews.categories()
		for fileid in movie_reviews.fileids(category)]

	random.shuffle(documents)

	all_words = []
	for w in movie_reviews.words():
	    all_words.append(w.lower())

	all_words = nltk.FreqDist(all_words)
	
	global word_featuresSent
	word_featuresSent = list(all_words.keys())[:3000]

	featuresets = [(findFeaturesSentiment(rev), category) for (rev, category) in documents]
	
	training_set = featuresets[:1900]
	testing_set = featuresets[1900:]

	sentimentClassifier = nltk.NaiveBayesClassifier.train(training_set)

	print("Classifier accuracy percent:",(nltk.classify.accuracy(sentimentClassifier, testing_set))*100)

	return sentimentClassifier

try:

############################## Prepare Classifiers

	# Train the classifiers
	
	# for a classifier
	# get training set


#	arsenalClassifier = prepareClassifier('trainingSetArsenal.json',"ARSENAL")
#	leicesterClassifier = prepareClassifier('trainingSetLeicester.json')
#	manCityClassifier = prepareClassifier('trainingSetManCity.json')
	manUnitedClassifier = prepareClassifier('trainingSetManUnited.json',"MANUNITED")
#	totenhamClassifier = prepareClassifier('trainingSetTotenham.json')
#	crystalPalaceClassifier = prepareClassifier('trainingSetCrystalPalace.json')
#	watfordClassifier = prepareClassifier('trainingSetWatford.json')
#	westHamClassifier = prepareClassifier('trainingSetWestHam.json')
#	liverpoolClassifier = prepareClassifier('trainingSetLiverpool.json')
#	evertonClassifier = prepareClassifier('trainingSetEverton.json')
#	arsenalClassifier = prepareClassifier('trainingSetArsenal.json')
#	arsenalClassifier = prepareClassifier('trainingSetArsenal.json')
#	arsenalClassifier = prepareClassifier('trainingSetArsenal.json')
#	arsenalClassifier = prepareClassifier('trainingSetArsenal.json')
#	arsenalClassifier = prepareClassifier('trainingSetArsenal.json')
#	arsenalClassifier = prepareClassifier('trainingSetArsenal.json')
	norwichClassifier = prepareClassifier('trainingSetNorwich.json',"NORWICH")
#	arsenalClassifier = prepareClassifier('trainingSetArsenal.json')
#	arsenalClassifier = prepareClassifier('trainingSetArsenal.json')
	
#	sentimentClassifier = prepareClassifier('trainingSetSentiment.json')
	sentimentClassifier = prepareSentimentClassifier()


###################################	

	auth = login()

	# get today's file
	with open('matches.json') as data_file:
		data = json.load(data_file)

		for match in data["matches"]:

			#t = Thread(target=myfunc, args=(1,))			
			#t = Thread(target=listenToStream, args=("a",))
			#t = Thread(target=listenToStream, kwargs={'match': match})
			#t.start()
			#print(json.dumps(match))
			_thread.start_new_thread( listenToStream, (match, ) )

		#_thread.start_new_thread( print_time, ("Thread-2", 4, ) )


except Exception as e:
	print(type(e))    # the exception instance
	print(e.args)     # arguments stored in .args
	print(e)

while 1:
	pass
