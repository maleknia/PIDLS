# -*- coding: utf-8 -*-
"""
Created on Sun May  2 21:35:01 2021

@author: PaNi
"""

#nltk.download("punkt")
#nltk.download('twitter_samples')
#nltk.download('stopwords')
#nltk.download('wordnet').
#nltk.download('averaged_perceptron_tagger')

#import cn

import Reddit_API_Connector as connector
import re
import CoinMarketCap_Connector as CMCConnector
from nltk.tag import pos_tag
import collections

from datetime import datetime
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re, string
import functools
import operator
from collections.abc import Iterable

import pandas as pd    
import pymysql
from sqlalchemy import create_engine


keys_file = open("Codes.txt")
lines = keys_file.readlines()
myRedditkey1 = lines[0].rstrip()
myRedditkey2 = lines[1].rstrip()
myUser_agent = lines[2].rstrip()
myUsername = lines[3].rstrip()
myPassword = lines[4].rstrip()

myDBName = lines[17].rstrip()
myDBUser = lines[18].rstrip()
myDBPass = lines[19].rstrip()
myDBAddress = lines[20].rstrip()
myDBPort = lines[21].rstrip()


import praw 
myReddit = praw.Reddit(client_id=myRedditkey1, \
                         client_secret=myRedditkey2, \
                         user_agent=myUser_agent, \
                         username=myUsername, \
                         password=myPassword)
    
myReddit = myReddit.subreddit("CryptoCurrency")


def tokenize(obj):
    if obj is None:
        return None
    elif isinstance(obj, str): # basestring in python 2.7
      
        return word_tokenize(obj)
    elif isinstance(obj, list):
        a = []
        for i in obj:
            #i = removeURL(i)            
            a.append(tokenize(i))
        return a
    else:
        return obj
    

def tokenize_list(obj):
    if obj is None:
        return None
    elif isinstance(obj, str): # basestring in python 2.7     
        return word_tokenize(obj)
    elif isinstance(obj, list):
        a = []
        for i in obj:
            #i = removeURL(i)            
            a.append(tokenize(i))
        return a
    else:
        return obj



def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    try:
        for word, tag in pos_tag(tokens):
            if tag.startswith('NN'):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'
            lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
        return lemmatized_sentence
    except:
        None

def lemmatize_sentence_list(list_of_tokens):
    myList = []
    for tokens in list_of_tokens:
        myList.append(lemmatize_sentence(tokens))        
    return myList


def remove_noise(inputs, stop_words = ()):

    cleaned_tokens = []
    
    try:
        for token, tag in pos_tag(inputs):
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                           '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
            token = re.sub("(@[A-Za-z0-9_]+)","", token)
    
            if tag.startswith("NN"):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'
    
            lemmatizer = WordNetLemmatizer()
            token = lemmatizer.lemmatize(token, pos)
    
            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
        return cleaned_tokens
    except:
        None
        
def getCoinList():
    myTemp = CMCConnector.getCoinNames()
    myCoinList =[]
    for coin in myTemp:
        coinName = coin['name'].lower()
        coinSymbol = coin['symbol'].lower()
        
        
        myCoinList.append([coinName,coinSymbol])
        
    
    return myCoinList



def getAlltheWordsthatareCoin (listofWords,listofCoins):
    allwords = []
    listofCoins = functools.reduce(operator.iconcat, listofCoins, []) #to make the coin list flat
    #listofCoins = lowercaseList(listofCoins)
    for tokens in listofWords:
        if isinstance(tokens[1], Iterable): 
            for token in tokens[1]:
                if token in listofCoins:
                    allwords.append(token)
                
    return allwords
    

removed_coins_hamed = ['get', 'like', 'go', 'time', 'one', 'buy', 'post', 'use', 'coin', 'day', 'lot', 'start', 'try', 'new', 'many', 'let', 'keep', 'well', 'help', 'put', 'may', 'value', 'long', 'world', 'call', 'trade', 'ask', 'best', 'next', 'pay', 'part', 'win', 'data', 'share', 'base', 'whole', 'idea', 'move', 'bank', 'sure', 'fund', 'bit', 'add', 'hard', 'stop', 'cash', 'free', 'space', 'hope', 'news', 'live', 'cap', 'fact', 'send', 'open', 'kind', 'sub', 'link', 'far', 'meme', 'rich', 'medium', 'job', 'token', 'care', 'chart', 'smart', 'love', 'daily', 'save', 'play', 'earn', 'fast', 'hit', 'bear', 'watch', 'note', 'name', 'dip', 'matter', 'simple', 'easy', 'team', 'game', 'rise', 'wish', 'fun', 'quick', 'hodl', 'lead', 'build', 'credit', 'limit', 'red', 'must', 'act', 'whale', 'face', 'deal', 'party', 'card', 'strong', 'hand', 'sign', 'paper', 'linear', 'gold', 'net', 'deep', 'solve', 'near', 'fine', 'bot', 'type', 'sense', 'basic', 'raise', 'decent', 'lol', 'eye', 'block', 'reserve', 'peak', 'vote', 'ok', 'sale', 'mass', 'cover', 'contribute', 'vision', 'meet', 'burn', 'aim', 'force', 'bullshit', 'fair', 'compound', 'request', 'proud', 'white', 'index', 'treat', 'equal', 'launch', 'carry', 'load', 'room', 'water', 'status', 'chat', 'flow', 'secret', 'dynamic', 'relevant', 'publish', 'yield', 'climb', 'shake', 'spike', 'tag', 'light', 'dad', 'baby', 'aave', 'planet', 'believer', 'infinity', 'liquid', 'stabilize', 'salt', 'diamond', 'rank', 'pizza', 'chicken', 'dark', 'blink', 'resistance', 'weather', 'giant', 'lightning', 'uber', 'popcorn', 'smoke', 'cook', 'handy']
removed_coins_scott = ['post', 'coin', 'day', 'start', 'try', 'help', 'put', 'may', 'call', 'next', 'set', 'real', 'whole', 'move', 'bit', 'add', 'cash', 'news', 'live', 'fact', 'send', 'kind', 'sub', 'care', 'chart', 'love', 'daily', 'save', 'watch', 'note', 'trust', 'simple', 'team', 'rise', 'wish', 'safe', 'hodl', 'credit', 'alt', 'face', 'deal', 'party', 'hand', 'sign', 'ath', 'deep', 'bot', 'defi', 'bet', 'hype', 'type', 'sense', 'ton', 'cut', 'raise', 'fud', 'decent', 'eye', 'tend', 'luck', 'bubble', 'vote', 'ok', 'pop', 'satoshi', 'contribute']

removed_coins = removed_coins_scott

    
stop_words = stopwords.words('english')
stop_words = stop_words
myCoinList_tuple = getCoinList()
myCoinList = functools.reduce(operator.iconcat, myCoinList_tuple, []) 


#Removing all the common words
myCoinListClean = []
for coinName in myCoinList:    
    if not coinName in stop_words and not coinName in removed_coins:
        myCoinListClean.append(coinName)
        
#Updating the Coinlist Tuple (raw list from function)        
for coinName in myCoinList_tuple:
    if coinName[0] not in myCoinListClean or coinName[1] not in myCoinListClean:
        myCoinList_tuple.remove(coinName)

#getting list of coins
myCoinList = myCoinListClean 

#prepping all the variabls before for live loop
starttime = datetime.now()
myCapturedCoins = []
countofrestart=0
outputDF = pd.DataFrame()
mySQLREPLICADF = pd.DataFrame()

#prepping mySQL engine
#for DF
engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(myDBUser,myDBPass,myDBAddress,myDBName))

#for DB commands
#db = pymysql.connect(host=myDBAddress,user=myDBUser,password=myDBPass,charset='utf8', db = myDBName, port = myDBPort)
#cursor = db.cursor()
#cursor.execute("drop table if exists mentions")


for comment in myReddit.stream.comments(skip_existing=True): 
    #myComment = comment.body
    #myComment = myComment.lower()
    #myComment_tokenized = tokenize(myComment)    
    #myComment_clean = remove_noise(myComment_tokenized,stop_words) 

    myComment = comment.body.lower().split()
    list1_as_set = set(myCoinList)
    intersection = list1_as_set.intersection(myComment)
    intersection_as_list = list(intersection)    
    timely = datetime.utcfromtimestamp(comment.created_utc) 
    timely_utc = comment.created_utc
    lastTimeStamp = comment.created_utc
    
    if len(intersection_as_list)>0:        

        myCapturedCoins.extend(intersection_as_list)
        
    
    #identifying 60 seconds to wrap upp
    timeDiffz = datetime.now()-starttime     
    if timeDiffz.total_seconds()>=60:
        starttime = datetime.now()
        myOccurrences = collections.Counter(myCapturedCoins) #getting count of mentions of each coin and symbol separately
        myPartOccurCount = []
        for coinTuple in myCoinList_tuple:
            count = 0
            try:
                count = count + myOccurrences[coinTuple[0]]
                count = count + myOccurrences[coinTuple[1]]
            except  Exception as ex:
                print ("exception")
                print (ex)
            if count>0: #if 0 mentions we dont want it
                myPartOccurCount.append([coinTuple[0],coinTuple[1],count, timely_utc])      
        
        myCapturedCoins = []     #emptying lists to capture more
        outputDF = outputDF.append(myPartOccurCount, ignore_index=True) 

        myPartOccurCount = []
        countofrestart += 1
    
    if countofrestart>10:
        
        outputDF.columns= ['coinname','symbol','count','ts'] #just dedicating columns before loading to MYSQL        
        outputDF.to_sql('mentions', if_exists='append', con = engine,index= False) #loading it to mySQL
        countofrestart = 0
        
        mySQLREPLICADF = mySQLREPLICADF.append(outputDF)# replica of mySQL
        
        outputDF = pd.DataFrame() #restarting the dataframe again

        
        
        





#cursor = db.cursor()
#cursor.execute("drop table mentions" )
#data = cursor.fetchall()


engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(myDBUser,myDBPass,myDBAddress,myDBName))
engine.execute("drop table if exists mentions")


#data = cursor.fetchall()
        
outputDF.to_sql('mentions', if_exists='append', con = engine)