#Collective Twitter, Facebook, and Wiki Scraper 
#Author: Sarah Pan 

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import tweepy
import json
import urllib
import time
import datetime

# Facebook Authentication 
app_id = "773209056178611"
app_secret = "624823f48d334db393ae3ceb35453ccc"
page_id = ""

access_token = app_id + "|" + app_secret

# Twitter Authentication 
consumer_key = 'HlvVTeAT5zTWGkTFVDDaJlgB9'
consumer_secret = 'rBxivokL8UFYnJO4tXCmL6LMwaHcJqgjjZLBFQwxNnf352Sn7F'
access_key = '2757346759-F32SmwmeIAd1FchHAgAnr6aypQ9G4REYljy1Huf'
access_secret = 'gPQQ3U2fRTwUEROSGD2UxwGmCmbU5yE7YU72hdN4a2vuB'

filename = "top100_users.csv"

fb_screen_names = []
twitter_screen_names = []
wiki_screen_names = []

# stack overflow function
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# Exports a list of the top social media users to a csv file
def get_top_100():
	pages_fb = []
	pages_twitter = []
	pages_wiki = []
	
	with open(filename, 'w', newline = '') as file:
		userWriter = csv.writer(file, dialect='excel')
		userWriter.writerow(["Name", "Facebook", "Twitter", "Wikipedia"])

		for i in range(1,6):
			page = requests.get("http://fanpagelist.com/category/top_users/view/list/sort/followers/page" + str(i))
			soup = BeautifulSoup(page.content, 'html.parser')
			
			profiles = soup.find_all('div', class_="listing_profile")

			for profile in profiles:
				profile_page = requests.get("http://fanpagelist.com" + profile.find_all('a', href=re.compile("user"))[0]['href'])

				profile_soup = BeautifulSoup(profile_page.content, 'html.parser')

				description = profile_soup.find('span', id = "profile_description").get_text()

				if profile_soup.find('a', title="Facebook Fan Page"):
					fb = profile_soup.find_all('a', title="Facebook Fan Page")[0]['href']
					fb = fb[25:len(fb)-1]
				else:
					fb = ""

				if profile_soup.find('a', title="Twitter Profile"):
					twit = profile_soup.find_all('a', title="Twitter Profile")[0]['href']
					twit = twit[19:len(twit)]
				else:
					twit = ""

				if profile_soup.find('a', title="Wikipedia Article"):
					wiki = profile_soup.find_all('a', title="Wikipedia Article")[0]['href']
					wiki = wiki[29:len(wiki)]
				else:
					wiki = ""

				userWriter.writerow([description, fb, twit, wiki])

# Code adapted from Max Woolf; Facebook Page Post Scraper 
# full facebook scraper code accessible at: https://github.com/minimaxir/facebook-page-post-scraper
def request_until_succeed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL %s: %s" % (url, datetime.datetime.now()))
            print("Retrying.")

    return response.read().decode(response.headers.get_content_charset())

# Needed to write tricky unicode correctly to csv
def unicode_normalize(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
                            0xa0:0x20 })

def getFacebookPageFeedData(page_id, access_token, num_statuses):
    base = "https://graph.facebook.com/v2.6"
    node = "/%s/posts" % page_id 
    fields = "/?fields=message,link,created_time,type,name,id," + \
            "comments.limit(0).summary(true),shares,reactions" + \
            ".limit(0).summary(true)"
    parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
    url = base + node + fields + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    return data

def processFacebookPageFeedStatus(status, access_token):
    status_message = '' if 'message' not in status.keys() else \
            unicode_normalize(status['message'])

    return (status_message)

def get_all_fb(screen_names):
	#write the csv 
	with open('Facebook.csv', 'w', encoding='utf-8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(["User", "Facebook Posts"])

		for screen_name in screen_names[1:]:
			if screen_name == "":
				writer.writerow("")
			else: 
				statuses = getFacebookPageFeedData(screen_name, access_token, 100) #number of posts
				posts = [screen_name]
				for status in statuses['data']:
					posts.append(processFacebookPageFeedStatus(status, access_token))
				writer.writerow(posts)

# Code adapted from https://gist.github.com/yanofsky/5436496
def get_all_tweets(screen_names):
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#write the csv	
	with open('Twitter.csv', 'w', encoding='utf8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(["User", "Tweets"])

		for screen_name in screen_names[1:]:
			#initialize a list to hold all the tweepy Tweets
			alltweets = []	
			
			#make initial request for most recent tweets (200 is the maximum allowed count)
			new_tweets = api.user_timeline(screen_name = screen_name, count=100)
			
			#save most recent tweets
			alltweets.extend(new_tweets)

			outtweets = [screen_name]
			for tweet in alltweets:
				outtweets.append(tweet.text)

			writer.writerow(outtweets)

def get_all_wiki(pages):
	with open('Wikipedia.csv', 'w', encoding='utf8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(["Name", "Wikipedia Information"])

		for page in pages[1:]: 
			info = [page]
			bio = ""
			site = requests.get("https://en.wikipedia.org/wiki/" + page)
			soup = BeautifulSoup(site.content, 'html.parser')

			for p in soup.find_all('p'):
				info.append(p.text)
				
			writer.writerow(info)

def main():
	# get_top_100()

	with open(filename, newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			fb_screen_names.append(row[1])
			twitter_screen_names.append(row[2])
			wiki_screen_names.append(row[3])

	# Option 1: Generate csv of tweets
	get_all_tweets(twitter_screen_names)
	# Option 2: Generate csv of facebook posts
	get_all_fb(fb_screen_names)
	# Option 3: Generate csv of Wikipedia bios
	get_all_wiki(wiki_screen_names)

main()
