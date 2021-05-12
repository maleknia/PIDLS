# -*- coding: utf-8 -*-
"""
Created on Wed May 12 08:21:28 2021

@author: sm2983
"""

key="6ce54db0-fb65-47bf-9a21-81e0d20dc2cc"
#test key
#key="b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c"

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time

class MCData:
    data=[]
    def __init__(self):
        pass
    def loadData(self):
        start=1
        res=[]
        ldata=[]
        error=False;
        while start==1 or (len(res)==5000 and len(res)>0):
            res=self.loadDataFrom(start)
            if res==429:
                time.sleep(60)
                continue
            elif type(res)==int:
                break
            start+=len(res)
            ldata.append(res)
        if not error:
            self.data=ldata
            
            
    def loadDataFrom(self,start):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
        parameters = {
                'start':str(start),
                'limit':'5000'
                }
        headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': key
                }
        session = Session()
        session.headers.update(headers)
        data=[]
        try:
          response = session.get(url, params=parameters)
          data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
          print(e)
        if data['status']["error_code"]==0:
            return data['data']
        else:
            return data['status']["error_code"]
        
# WE NEED TO UPDATE the API plan to enable this
  #symbol BTC,...
  #start_time ISO 8601 timestamp
  #end_time ISO 8601 timestamp
  #interval "yearly" "monthly" "weekly" "daily" "hourly" "5m" "10m""15m""30m"
      #"45m""1h""2h""3h""4h""6h""12h""24h""1d""2d""3d""7d""14d""15d""30d""60d""90d""365d"
    def getChart(self,symbol,start_time,end_time,interval):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical'
        parameters = {
                'symbol':symbol,
                'time_start': start_time,
                'time_end': end_time,
                'interval':interval
            }
        headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': key
                }
        session = Session()
        session.headers.update(headers)
        data=[]
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        return data



obj=MCData();
data=obj.loadData()