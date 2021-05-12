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



import re, string
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import FreqDist






#myReddit = connector.ApiConnector.RetrieveRedditDF(ReadLimit=2000,FileSaveAs="Cache1.csv")
myReddit = pd.read_csv('FileSaveAs.csv')
myCoinList = cn.getNames()

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
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence




def remove_noise(inputs, stop_words = ()):

    cleaned_tokens = []

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

def is_nan(x):
    return (x != x)



def processWords(inputList,inputStopWords):
    
    myTokenizedList = tokenize(inputList)   
    returnList=[]    
    for i in myTokenizedList:
        if not is_nan(i):
            returnList.append(remove_noise(i,inputStopWords))
    return returnList
    
            
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token




#Main
stop_words = stopwords.words('english')
myRedBody_Clean = processWords(myRedBodyList,stop_words)
myRedTitle_Clean = processWords(myRedTitleList,stop_words)


all_pos_words = get_all_words(myRedBody_Clean)
freq_dist_pos = FreqDist(all_pos_words)
print(freq_dist_pos.most_common(100))