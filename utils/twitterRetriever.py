import tweepy
import json
import codecs

rawLines = open("NAACL_SRW_2016.csv","r").read().split("\n")

consumer_key = "hJtIQV3mZm8f8YbLBaBNxijun"
consumer_secret = "dO7oHGDIFzdDxV8MgnIWleiLyHNLfhQYfdw8ZHyEZ3gqUrIox3"
access_token = "252634999-y0obLLq7UbWx6fEchaGKJhqLWxRDUjBJhSnxn2DX"
access_token_secret = "7u4z2AhUF90yKWlE38FLfDmUeyZUAYmIsXQpEwjRRvvuX"


def retrieve_tweets(tweetIdList, labelList, api):
	path = "/home/joan/Escritorio/Datasets/hateSpeech/hatespeech-master/extracted/"
	tweetList = api.statuses_lookup(tweetIdList)
	for idx, tweet in enumerate(tweetList):
		text = tweet.text
		tweetId = tweetIdList[idx]
		label = labelList[idx]
		out = codecs.open(path+tweetId+"_"+label,"w", encoding="utf-8")
		out.write(text)
		out.close()



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweetIdList = []
labelList = []

for line in rawLines:
	tweetId, label = line.split(",")	
	tweetIdList.append(tweetId)
	labelList.append(label)			
	if len(tweetIdList) == 100:
		retrieve_tweets(tweetIdList, labelList, api)
		tweetIdList = []
		labelList = []

