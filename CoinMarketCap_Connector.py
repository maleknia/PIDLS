from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class CoinMarketCapAPI:
    keys_file = open("Codes.txt")
    lines = keys_file.readlines()
    ConMarketAPI = lines[14].rstrip()
    
def getCoinNames():
    
    keys_file = open("Codes.txt")
    lines = keys_file.readlines()
    ConMarketAPI = lines[14].rstrip()
      
        
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': ConMarketAPI,
    }
    
    
    start = 1
    limit = 5000
    convert = 'USD'
    
    parameters = {
      'start':str(start),
      'limit':str(limit),
      'convert':convert
    }
    
    session = Session()
    session.headers.update(headers)
    
    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
      
    alldata =  data['data']
    extension = 0
    
    while len(data['data']) == 5000:  
        extension =+ 1
        start = (extension*limit)+1 #so it starts from 5001 and so on
        parameters = {
          'start':str(start),
          'limit':str(limit),
          'convert':convert
        }
        session = Session()
        session.headers.update(headers)
        
        try:
          response = session.get(url, params=parameters)
          data = json.loads(response.text)
          #print(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
          print(e)
          
        alldata = alldata +  data['data']
        
        if extension>20: #noway we get that many coins
            break
        
        
    return alldata
        
        
        
            
          
