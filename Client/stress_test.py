import requests
import random
import pandas as pd
import time

from threading import Thread

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

def thread_function(tNum):
    print "Loading sample data in thread %d..."%tNum
    rand_part_num = random.randint(1,2)

    tweet_data = pd.read_csv('./TwitterData/tweets_part%d.csv'%rand_part_num)

    base_url = 'http://192.168.56.101:8080/api/'
    req_types = ['login/','register/','tweet/','findTweetsByHashtag/','findTweetsByMentions/']

    hashtags = getHashtags(tweet_data['tweet'])
    mentions = getMentions(tweet_data['tweet'])

    n_data = len(tweet_data.user)
    n_hashtags = len(hashtags)
    n_mentions = len(mentions)

    while True:
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

response = requests.get("http://192.168.56.101:8080/api/startStressTest")
print response
n_threads = 50
while n_thread>0:
    t = Thread(target=thread_function, args=(51-n_thread,))
    t.start()

t1 = current_milli_time()

while True:
    if current_milli_time() - t1 > 10000:
        break

response = requests.get("http://192.168.56.101:8080/api/endStressTest")
print response
