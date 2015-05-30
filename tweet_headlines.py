#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import bbcmarkovlib as bml
import time

token = config.token
token_key = config.token_key
con_secret = config.con_secret
con_key= config.con_key

url_address = 'http://feeds.bbci.co.uk/news/rss.xml'
max_sentence_chars = 140 #for twitter ofc

hours_to_tweet_news = [8,12,18,22] #time at which to tweet number_of_stories
number_of_stories = 5
gmt_offset = +1 #so that hours are valid

try:
    import twitter
except ImportError:
    try:
        print 'twitter module not found, trying to install...'
        from setuptools.command import easy_install
        easy_install.main(['-U','twitter'])
        import twitter
    except ImportError:
        print 'please download module from:'
        print 'http://mike.verdone.ca/twitter/#install'
        print 'easy_install not present :('

def postToTwitter(message):
    try:
        twit = twitter.Twitter(auth=twitter.OAuth(token, token_key, con_key, con_secret))
        if len(message) <= 140:
            try:
                twit.statuses.update(status=message)
            except twitter.TwitterHTTPError:
                print 'Failed to post tweet'
        else:
            try:
                twit.statuses.update(status=message[:139])
            except twitter.TwitterHTTPError:
                print 'Failed to post tweet'
    except:
        print 'Some error occurred posting to twitter...'


last_tweeted_hour = -1

try:
	while True:
		print 'testing'
		current_hour = int(time.strftime("%H", time.gmtime()))+gmt_offset
		if current_hour in hours_to_tweet_news and last_tweeted_hour != current_hour:
			titledata,descdata = bml.processUrl(url_address)
			descdataset = bml.genSetOfWords(descdata)
			markov_graph = bml.genMarkov(descdata,descdataset)
			print 'The news at '+str(current_hour%12)+' o\'clock:'
			for i in range(number_of_stories):
				while True:
					result = bml.processSentence(bml.genSentence(markov_graph))
					if len(result)<141:
						print result
						postToTwitter(result)
						break
				time.sleep(60)
			last_tweeted_hour = current_hour


		time.sleep(60)

except KeyboardInterrupt:
	print 'Closing...'