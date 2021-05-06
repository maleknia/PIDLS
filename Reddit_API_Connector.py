# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 23:51:15 2021

@author: PaNi
"""

#! usr/bin/env python3


import praw
import pandas as pd
import datetime as dt

class ApiConnector:
    
    
    keys_file = open("Codes.txt")
    lines = keys_file.readlines()
    myRedditkey1 = lines[0].rstrip()
    myRedditkey2 = lines[1].rstrip()
    myUser_agent = lines[2].rstrip()
    myUsername = lines[3].rstrip()
    myPassword = lines[4].rstrip()
    

    

    
    #https://www.storybench.org/how-to-scrape-reddit-with-python/?fbclid=IwAR0EoyFD2oFqCxElz9NjjVs2FpLLjcybrb3Oli1kjwbdAWz7IjL9eZRRSCQ
    
    myReddit = praw.Reddit(client_id=myRedditkey1, \
                         client_secret=myRedditkey2, \
                         user_agent=myUser_agent, \
                         username=myUsername, \
                         password=myPassword)
    
    
    def RetrieveRedditDF(RedditAgent=myReddit, SubReddit="CryptoCurrency", ReadLimit=500, FileSaveAs = None):
            
            
            mySubreddit = RedditAgent.subreddit(SubReddit)
            myTopSubReddit = mySubreddit.top(limit=ReadLimit)
        
        
        
            topics_dict = { "title":[],                 
                           "score":[],
                           "id":[], 
                           "url":[],
                            "comms_num": [], 
                            "created": [], 
                            "body":[]}
            
            for mySubmitted in myTopSubReddit:
                topics_dict["title"].append(mySubmitted.title)
                topics_dict["score"].append(mySubmitted.score)
                topics_dict["id"].append(mySubmitted.id)
                topics_dict["url"].append(mySubmitted.url)
                topics_dict["comms_num"].append(mySubmitted.num_comments)
                topics_dict["created"].append(mySubmitted.created)
                topics_dict["body"].append(mySubmitted.selftext)
                
            topics_data = pd.DataFrame(topics_dict)
            
            def get_date(created):
                return dt.datetime.fromtimestamp(created)
            
            _timestamp = topics_data["created"].apply(get_date)    
            topics_data = topics_data.assign(timestamp = _timestamp)
            
            if FileSaveAs==None:
                return topics_data
            else:
                topics_data.to_csv('FileSaveAs', index=False) 














