#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import csv
import json

# Twitter API credentials

with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

# Create the api endpoint

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

# Mention the maximum number of tweets that you want to be extracted.

maximum_number_of_tweets_to_be_extracted = int(input('Enter the number of tweets that you want to extract- '))

# Mention the hashtag that you want to look out for

hashtag = input('Enter the hashtag you want to scrape- ')

list_of_tweets = []
for tweet in tweepy.Cursor(api.search, q='#' + hashtag, lang='en', tweet_mode='extended', rpp=100).items(maximum_number_of_tweets_to_be_extracted):
    list_of_tweets.append(tweet)

outtweets = []
tweet_vals = []
for tweet_info in list_of_tweets:
    if 'retweeted_status' in dir(tweet_info):
        if (tweet_info.retweeted_status.full_text not in tweet_vals):
            tweet_vals.append(tweet_info.retweeted_status.full_text)
            tweet=tweet_info.retweeted_status.full_text
            this_tweet = [tweet_info.id_str, tweet_info.created_at, tweet.encode('utf-8')]
            outtweets.append(this_tweet)
    else:
        if (tweet_info.full_text not in tweet_vals):
            tweet_vals.append(tweet_info.full_text)
            tweet=tweet_info.full_text
            this_tweet = [tweet_info.id_str, tweet_info.created_at, tweet.encode('utf-8')]
            outtweets.append(this_tweet)

with open('tweets_with_hashtag_' + hashtag + '.csv', 'w', encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'created_at', 'text'])
    writer.writerows(outtweets)

print ('Extracted ' + str(maximum_number_of_tweets_to_be_extracted) + ' tweets with hashtag #' + hashtag)