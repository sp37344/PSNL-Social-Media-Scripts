#Twitter Hashtag Collector Program 
#Author: Sarah Pan 

import datetime
import re
import json 
import copy 
import csv
import pickle
import tweepy
from tweepy import OAuthHandler

#TASKS:
#change camelCase to readable form 
#extract tweets
#loop consumer key input if incorrect
#facebook webscraping 

#Function taken from stack overflow -- checks if ascii
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

#gets all woeid values for US locations
def woeid_collector(api):
	USA_woeids = []

	for location in api.trends_available():
		if location["country"] == "United States":
			USA_woeids.append(location["woeid"])

	with open("trending_hashtags_woeid", 'wb+') as outfile:
	    pickle.dump(USA_woeids, outfile)

#gets the most popular hashtags in the locations
def hashtag_collector(api):
	USA_woeids = []
	trend_tags = []	
	trend = ""

	with open("trending_hashtags_woeid", 'rb') as infile:
	    USA_woeids = pickle.load(infile)

	for i in USA_woeids:	
	#	print(i)
		for trend in api.trends_place(int(i)):		
			for j in trend['trends']:
				if j['name'][0] == '#':
					trend_tags.append(j['name'][1:])
				else:
					trend_tags.append(j['name'])

	with open("trending_hashtags", 'wb+') as outfile:
	    pickle.dump(trend_tags, outfile)

#exports the list of hashtags to csv
def csv_converter(api):
	hashtags = []
	filtered_hashtags = []
	now = datetime.datetime.now().date()

	with open("trending_hashtags", 'rb') as infile:
	    hashtags = pickle.load(infile)

	print(u'bats\xc1'.encode('utf-8'))

	for tag in list(set(hashtags)):
		if is_ascii(tag):
			print(tag)
			filtered_hashtags.append(tag)

	file_name = "trending_hashtags_" + str(now) + ".csv"
	with open(file_name, 'w+', newline = '') as file:
		tweetWriter = csv.writer(file, dialect='excel')
		for tag in filtered_hashtags:
			tweetWriter.writerow([tag])

def main():
	print("Login (press enter to use default login)")
	consumer_key = input("Enter consumer key: ")

	if consumer_key == '':
		consumer_key = 'HlvVTeAT5zTWGkTFVDDaJlgB9'
		consumer_secret = 'rBxivokL8UFYnJO4tXCmL6LMwaHcJqgjjZLBFQwxNnf352Sn7F'
		access_token = '2757346759-F32SmwmeIAd1FchHAgAnr6aypQ9G4REYljy1Huf'
		access_secret = 'gPQQ3U2fRTwUEROSGD2UxwGmCmbU5yE7YU72hdN4a2vuB'
	else:
		consumer_secret = input("Enter consumer secret: ")
		access_token = input("Enter access token: ")
		access_secret = input("Enter access secret: ")

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	 
	api = tweepy.API(auth)

	#Step 1: extract woeid for each region
	#can comment out step 1 and 2 (woeid_collector() and #hashtag_collector()) when twitter quota is exceeded
	woeid_collector(api)
	#Step 2: collect hashtags for each region 
	hashtag_collector(api)
	#Step 3: convert data to csv 
	csv_converter(api)

main()