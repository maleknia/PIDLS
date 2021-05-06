# -*- coding: utf-8 -*-
"""
Created on Sun May  2 21:35:01 2021

@author: PaNi
"""

import cn
import Reddit_API_Connector as connector
import nltk
import pandas as pd

#nltk.download("punkt")
#nltk.download('twitter_samples')


myReddit = connector.ApiConnector.RetrieveRedditDF()
#myReddit = pd.read_csv('FILENAME.csv')
myCoinList = cn.getNames()

myRedList = myReddit['title']
    

from nltk.corpus import twitter_samples

positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
text = twitter_samples.strings('tweets.20150430-223406.json')