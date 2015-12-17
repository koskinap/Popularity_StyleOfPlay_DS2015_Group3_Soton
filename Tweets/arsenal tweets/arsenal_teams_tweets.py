import tweepy
import csv

import sys
import os

import json

from os import listdir
from os.path import isfile, join

ACCESS_TOKEN = '1681062247-YXE4HfZCwLWBhE7SvNL2TmNC2vwHsBFH6Zvtjyb'
ACCESS_SECRET = 'b9cjJxoO8ZwnUTIvnySk8VoZklm3MQpsU3jqEqlTBhOP3'
CONSUMER_KEY = 'VCwBAlUbXs8uCLkpHTOLYiOCl'
CONSUMER_SECRET = '4R06f1I5K1Vmj9b5i4IbrB3xifrD96IIHSxactyMypT3w9ce7k'

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)


# get files in the tweets directory
path = 'files/'
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

fileName = ''
sinceId = None
max_id = -1L

if not onlyfiles:
 	print "First Time"
	fileName = '1'

else:
	max = '0'

	for tweetsFile in onlyfiles:
		if tweetsFile > max:
			max = tweetsFile

	fileName = str(int(max)+1)
	lastFile = open(path+max, 'r')
	lastTweet = lastFile.readline()
	sinceId = json.loads(lastTweet)['id']+1
	print 
	
searchQuery = 'arsenal'
maxTweets = 10000000
tweetsPerQry = 50



tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(path+fileName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:

		_tweet = {}
		_tweet['id'] = tweet.id
		_tweet['created_at'] = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
		_tweet['text'] = tweet.text
		_tweet['coordinates'] = tweet.coordinates
		_tweet['geo'] = tweet.geo
		if tweet.place is None:
			_tweet['country'] = None
		else:
			_tweet['country'] = tweet.place.country
		json_tweet = json.dumps(_tweet)
                f.write(json_tweet+'\n')

            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, path+fileName))

