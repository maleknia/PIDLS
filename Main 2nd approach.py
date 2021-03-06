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
import CoinMarketCap_Connector as CMCConnector
import Reddit_API_Connector as connector
import nltk
import pandas as pd
from collections.abc import Iterable

from datetime import datetime
import time

import re, string
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import FreqDist


import functools
import operator

import csv


def removeURL(obj):
    try:
        return re.sub(r'http\S+', '', obj)
    except:
        return obj

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
        obj = removeURL(obj)
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

def remove_noise_list(inputList,stop_list):
    myList = []
    for item in inputList:
        myList.append(remove_noise(item,stop_list))
    return myList



def is_nan(x):
    return (x != x)


"""
def processWords(inputList,inputStopWords):    #Tokenize AND remove noises from a list
    myTokenizedList = tokenize(inputList)   
    returnList=[]    
    for i in myTokenizedList:
        if not is_nan(i):
            returnList.append(remove_noise(i,inputStopWords))
    return returnList
"""
            
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_text_ready_for_model(cleaned_tokens_list):
    myList = []
    for clean_list in cleaned_tokens_list:
        myMiniList = []
        if isinstance(clean_list, Iterable): 
            for token in clean_list:
                myMiniList.append([token, True])
        myList.append(dict(myMiniList))
    return myList


def get_text_ready_for_model_simpleEntity(clean_list):
        myList = []    
        myMiniList = []
        if isinstance(clean_list, Iterable): 
            for token in clean_list:
                myMiniList.append([token, True])
        myList = (dict(myMiniList))
        return myList
            


def runModelonTextList(model,textlist):
    print("hi")
    for text in textlist:
        result = model.classify(text)
        print(text)
        print(result)
        yield [text,result]



def sentimentAnalysis(textList,inputStop_list):
    myResult = []
    for myEntity in textList:
            myEntity = myEntity.lower()
            myEntity_tokenized = tokenize(myEntity)    
            myEntity_clean = remove_noise(myEntity_tokenized,stop_words)
            myEntity_norlmalized = lemmatize_sentence(myEntity_clean)
            #myEntity_for_model = get_text_ready_for_model_simpleEntity(myEntity_norlmalized)
            #result = myClassifier.classify(myEntity_for_model)
            myResult.append(myEntity_norlmalized)
            
    return myResult
            

def getAlltheWords (listofWords):
    allwords = []
    for tokens in listofWords:
        if isinstance(tokens[1], Iterable): 
            for token in tokens[1]:
                allwords.append(token)
                
    return allwords

def lowercaseList (listofCoins): #make it a lowercase
    result =[]
    for i in listofCoins:
        result.append(i.lower())
    return result
        

def getAlltheWordsthatareCoin (listofWords,listofCoins):
    allwords = []
    listofCoins = functools.reduce(operator.iconcat, listofCoins, []) #to make the coin list flat
    listofCoins = lowercaseList(listofCoins)
    for tokens in listofWords:
        if isinstance(tokens[1], Iterable): 
            for token in tokens[1]:
                if token in listofCoins:
                    allwords.append(token)
                
    return allwords


def getCountofMentionedCoinsinComments (listofComments,listofCoins, returncoinnames = False):
    #in list of comments first argument is TS and second is the comment
    result = []
#    listofCoins = functools.reduce(operator.iconcat, listofCoins, []) #to make the coin list flat
#    listofCoins = lowercaseList(listofCoins)
    for comment in listofComments:
        count = 0
        if isinstance(comment[1], Iterable): 
            for word in comment[1]:
                if word in listofCoins:
                    count = count + 1
                    
        if returncoinnames:
            result.append([listofCoins,comment[0],count])
        else:
            result.append([comment[0],count])
                
    return result


def getTheTotalCountofCountedCoins(myCoinList, freq_dist_pos):
    result = []
    for words in myCoinList:
        count = 0
        try:
            count = freq_dist_pos[words[0]]
            count = count + freq_dist_pos[words[0]]
            result.append([words[0],words[1],count])
        except:
            None
    return result


""" Running all comments in reddits

def extractReditComments(listofReddits):
    result = []
    count = 0
    for i in listofReddits:
        
        myComments = connector.ApiConnector.RetriveRedditComment( redID= i) #extracting comments for a whole Reddit
        for comment in myComments:
            parsed_date = datetime.utcfromtimestamp(comment.created_utc)
            parsed_date = str(parsed_date.year)+'-'+str(parsed_date.month)+'-'+str(parsed_date.day)
            if comment.body != '[removed]':
                result.append([comment.body, parsed_date])
        
                
        with open("Comments_"+str(count)+".csv", 'w',encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(result)
        result = []
        count += 1        
        

        
    #return result
                



start_time = time.time()
myComments = extractReditComments(myReddit['id'].tolist())
print("--- %s seconds ---" % (time.time() - start_time))
"""

#myComments = extractReditComments(myReddit['id'].tolist())
#myComments = connector.ApiConnector.RetriveRedditComment(redID='7jrba2')


    

#myReddit = connector.ApiConnector.RetrieveRedditDF(ReadLimit=2000,FileSaveAs="Cache1.csv")
#myReddit = pd.read_csv('FileSaveAs.csv')
#myCoinList = cn.getNames()



"""
myRedbodyTokens = tokenize(myRedBodyList)
myRedtitleTokens = tokenize(myRedTitleList)

myRedbodyTokensNormal = lemmatize_sentence_list(myRedbodyTokens)
myRedtitleTokensNormal = lemmatize_sentence_list(myRedtitleTokens)

myRedbody_Tokens_Normal_Clean = remove_noise_list(myRedbodyTokensNormal,stop_words)
myRedtitle_Tokens_Normal_Clean = remove_noise_list(myRedtitleTokensNormal,stop_words)


myRedBody_for_model = get_text_ready_for_model(myRedbody_Tokens_Normal_Clean)
myRedTitle_for_model = get_text_ready_for_model(myRedtitle_Tokens_Normal_Clean)
"""

#frequency
#all_pos_words = get_all_words(myRedBody_Clean)
#freq_dist_pos = FreqDist(all_pos_words)

     
#Trainig positive negative based on positive negative tweets
"""  
positive_tweet_tokens = tokenize(twitter_samples.strings('positive_tweets.json'))
negative_tweet_tokens = tokenize(twitter_samples.strings('negative_tweets.json'))

positive_tweet_normal = lemmatize_sentence_list(positive_tweet_tokens)
negative_tweet_normal = lemmatize_sentence_list(negative_tweet_tokens)

positive_tweet_clean = remove_noise_list(positive_tweet_normal,stop_words)
negative_tweet_clean = remove_noise_list(negative_tweet_normal,stop_words)


positive_tokens_for_model = get_text_ready_for_model(positive_tweet_tokens)
negative_tokens_for_model = get_text_ready_for_model(negative_tweet_tokens)

import random

positive_dataset = [(tweet_dict, "Positive")
                     for tweet_dict in positive_tokens_for_model]

negative_dataset = [(tweet_dict, "Negative")
                     for tweet_dict in negative_tokens_for_model]

dataset = positive_dataset + negative_dataset

random.shuffle(dataset)

train_data = dataset[:7000]
test_data = dataset[7000:]


from nltk import classify
from nltk import NaiveBayesClassifier
myClassifier = NaiveBayesClassifier.train(train_data)

print("Accuracy is:", classify.accuracy(myClassifier, test_data))

print(myClassifier.show_most_informative_features(10))



#resulty = runModelonTextList(myClassifier, myRedBody_for_model)

"""
            
    

#myResultBody = sentimentAnalysis(myRedBodyList,stop_words)
#myResultTitle = sentimentAnalysis(myRedTitleList,stop_words)




#Main

stop_words = stopwords.words('english')

start_time = time.time()
#myReddit = connector.ApiConnector.RetrieveRedditDF(ReadLimit=2000) #extracting posts
print("--- %s seconds to load Reddit ---" % (time.time() - start_time))


### Getting  coin list
myTemp = CMCConnector.getCoinNames()
myCoinList =[]
for coin in myTemp:
    myCoinList.append([coin['name'].lower(),coin['symbol'].lower()])

start_time = time.time()
myRedditComments = pd.read_csv('all.csv')
myRedditComments.columns = ['comment', 'TS']
myRedComments = myRedditComments[~myRedditComments['comment'].isnull()]
myRedComments = myRedditComments[~myRedditComments['TS'].isnull()]
myRedComments['TS']= myRedComments['TS'].astype(str)
myRedComments['comment']= myRedComments['comment'].astype(str)

print (myRedComments.dtypes)

myRedComments['txt2']= myRedComments.groupby(['TS'])['comment'].transform(lambda x: ' '.join(x))
myRedGrp = myRedComments[['TS','txt2']].drop_duplicates()


myTokenizedList = sentimentAnalysis(myRedGrp['txt2'].tolist(),stopwords)

myTSTokenizedList = []
for TS, comment in zip(myRedGrp['TS'],myTokenizedList):
    myTSTokenizedList.append([TS,comment])
    

''' getting files for better visualization"
ScottResult = []

for coinin in myCoinList:
    print (coinin)
    myResult = getCountofMentionedCoinsinComments(myTSTokenizedList,coinin,True)    
    ScottResult.append(myResult)
    

import numpy as np
ScottSmall = []
count = 0
count2 = 0
'''


for miniScott in ScottResult:
    for miniScott2 in miniScott:
        
        ScottSmall.append([miniScott2[0][0],miniScott2[0][1],miniScott2[1],miniScott2[2]])   
        count += 1
    
    if count>900000:
        count2 +=1        
        np.savetxt('Scotts{}.csv'.format(count2),ScottSmall, delimiter = ',', fmt='% s',encoding='utf8')
        count = 0 
        ScottSmall = []
        


with open("shib.csv", 'w',encoding="utf-8") as f:
     writer = csv.writer(f)
     writer.writerows(myResult)


    

""" 


try:
    myRedTitleList = myReddit['title'].tolist()
    myRedBodyList = myReddit['body'].tolist()
except:
    None
















allwords = getAlltheWords(myResultBody)
allwords = getAlltheWordsthatareCoin(myResultBody,myCoinList)

freq_dist_pos = FreqDist(allwords)

#result2 = sentimentAnalysis(myRedBodyList,stop_words)          

listofCoins = functools.reduce(operator.iconcat, myCoinList, []) #to make the coin list flat
#listofCoins = lowercaseList(listofCoins)  #make them lower case like the list

#listofCoins = lowercaseList(myCoinList)

#freq_dist_pos = FreqDist(allwords)# finds the frequecy of coins



result = []
for words in myCoinList:
    count = 0
    try:
        count = freq_dist_pos[words[0]]
        count = count + freq_dist_pos[words[0]]
        result.append([words[0],words[1],count])
    except:
        None


coinCount = getTheTotalCountofCountedCoins(myCoinList,freq_dist_pos)
        


asd = freq_dist_pos.most_common()
print (asd)



with open("train_data.csv", 'w',encoding="utf-8") as f:
     writer = csv.writer(f)
     writer.writerows(result)

with open("needstoclean.csv", 'w',encoding="utf-8") as f:
     writer = csv.writer(f)
     writer.writerows(asd)



        

index = 0
result_list = []
for text in myRedBody_for_model:
    
    if isinstance(text, dict):        
        #if  bool(text): #if it is not empty            
            result = myClassifier.classify(text)
            result_list.append([result,text,myRedBodyList[index]])            
            
    index =+ 1



allwordswithCoin = []
listofCoins = functools.reduce(operator.iconcat, myCoinList, []) #to make the coin list flat
listofCoins = lowercaseList(listofCoins)
for tokens in allwords:
    for coinName in 
            if tokens in listofCoins:
                allwordswithCoin.append(tokens)

"""




