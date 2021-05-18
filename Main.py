# -*- coding: utf-8 -*-
"""
Created on Sun May  2 21:35:01 2021

@author: PaNi
"""

#nltk.download("punkt")
#nltk.download('twitter_samples')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')

import cn
import Reddit_API_Connector as connector
import nltk
import pandas as pd
from collections.abc import Iterable



import re, string
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import FreqDist






#myReddit = connector.ApiConnector.RetrieveRedditDF(ReadLimit=2000,FileSaveAs="Cache1.csv")
myReddit = pd.read_csv('FileSaveAs.csv')
#myCoinList = cn.getNames()

try:
    myRedTitleList = myReddit['title'].tolist()
    myRedBodyList = myReddit['body'].tolist()
except:
    None

def removeURL(obj):
    try:
        return re.sub(r'http\S+', '', obj)
    except:
        return obj

def tokenize(obj):
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
            


def runModelonTextList(model,textlist):
    print("hi")
    for text in textlist:
        result = model.classify(text)
        print(text)
        print(result)
        yield [text,result]

#Main
stop_words = stopwords.words('english')

myRedbodyTokens = tokenize(myRedBodyList)
myRedtitleTokens = tokenize(myRedTitleList)

myRedbodyTokensNormal = lemmatize_sentence_list(myRedbodyTokens)
myRedtitleTokensNormal = lemmatize_sentence_list(myRedtitleTokens)

myRedbody_Tokens_Normal_Clean = remove_noise_list(myRedbodyTokensNormal,stop_words)
myRedtitle_Tokens_Normal_Clean = remove_noise_list(myRedtitleTokensNormal,stop_words)


myRedBody_for_model = get_text_ready_for_model(myRedbody_Tokens_Normal_Clean)
myRedTitle_for_model = get_text_ready_for_model(myRedtitle_Tokens_Normal_Clean)


#frequency
#all_pos_words = get_all_words(myRedBody_Clean)
#freq_dist_pos = FreqDist(all_pos_words)

       
#Trainig positive negative based on positive negative tweets



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



custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."



#resulty = runModelonTextList(myClassifier, myRedBody_for_model)

index = 0
result_list = []
for text in myRedBody_for_model:
    
    if isinstance(text, dict):        
        #if  bool(text): #if it is not empty            
            result = myClassifier.classify(text)
            result_list.append([result,text,myRedBodyList[index]])            
            
    index =+ 1












