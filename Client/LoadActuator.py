# This script is used for testing requests. This scripts randomly fires REST API
# calls on the server to test its capacity to handle requests.
# To do that is loads one of the fragments of Twitter data from /TwitterData folder
# and randomly chooses one of the requests to fire on the server. To increase the
# volume of the requests one can run multiple instances of this program with different
# fragments of the data.

import requests
import random
import pandas as pd
import time

def getHashtags(tweets):
    hashtags = []
    for tweet in tweets:
        words = tweet.split()
        for word in words:
            if word[0] == '#':
                hashtags.append(word[1:])
    return hashtags
    pass

def getMentions(tweets):
    mentions = []
    for tweet in tweets:
        words = tweet.split()
        for word in words:
            if word[0] == '@':
                mentions.append(word[1:])
    return mentions

current_milli_time = lambda: int(round(time.time() * 1000))
print current_milli_time(), type(current_milli_time())

print "Loading sample data..."
rand_part_num = random.randint(1,2)

tweet_data = pd.read_csv('./TwitterData/tweets_part%d.csv'%rand_part_num)

base_url = 'http://localhost:8080/api/'
req_types = ['login/','register/','tweet/','findTweetsByHashtag/','findTweetsByMentions/']

hashtags = getHashtags(tweet_data['tweet'])
mentions = getMentions(tweet_data['tweet'])

n_data = len(tweet_data.user)
n_hashtags = len(hashtags)
n_mentions = len(mentions)

t1 = current_milli_time()
req_count = 0
print 'Actuating load...'

while current_milli_time()-t1 < 10500:
    req_type = random.randint(0,len(req_types)-1)
    if req_type == 0:
        rand_user = tweet_data.user[random.randint(0,n_data-1)]
        data = {'username':rand_user, 'password':rand_user}
        response = requests.post(base_url+req_types[req_type], data=data)
        #print '[LOGIN]',response.json()
    elif req_type == 1:
        rand_user = tweet_data.user[random.randint(0,n_data-1)]
        data = {'username':rand_user, 'password':rand_user}
        response = requests.post(base_url+req_types[req_type], data=data)
        #print '[REGISTER]',response.json()
    elif req_type == 2:
        idx = random.randint(0,n_data-1)
        rand_tweet_user = tweet_data.user[idx]
        rand_tweet = tweet_data.tweet[idx]
        rand_tweet_ts = tweet_data.timestamp[idx]
        data = {'username':rand_tweet_user, 'tweetText':rand_tweet, 'timestamp':rand_tweet_ts}
        response = requests.post(base_url+req_types[req_type], data=data)
        #print '[TWEET]',response.json()
    elif req_type == 3:
        idx = random.randint(0,n_hashtags-1)
        data = {'queryTag':hashtags[idx]}
        response = requests.post(base_url+req_types[req_type], data=data)
        #print '[TWEETS_BY_TAG]',response.json()
    else:
        idx = random.randint(0,n_mentions-1)
        data = {'queryMention':mentions[idx]}
        response = requests.post(base_url+req_types[req_type], data=data)
        #print '[TWEETS_BY_MENTION]',response.json()
    req_count += 1


print "Results:"
print "RPS count=", req_count*1.0/10
