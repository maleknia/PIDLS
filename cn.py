# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:34:17 2021

@author: sm2983
"""
import http.client
from html.parser import HTMLParser
class MyHTMLParser(HTMLParser):
    fnames=[]
    record=False
    maxPage=1
    cnt=0
    insideTheTable=False
    trn=0
    tdn=0
    def handle_starttag(self, tag, attrs):
        if tag=="table":
            a=[y for x,y in attrs if x=="class"]
            self.insideTheTable=len(a)>0 and "cmc-table cmc-table___11lFC" in a[0]
        if self.insideTheTable and tag=="tr":
            self.trn+=1
            self.tdn=0
        if self.insideTheTable and tag=="td":
            self.tdn+=1
            if self.tdn==3:
                self.record=True
                self.cnt=2

        if tag=="a":
            a=[y for x,y in attrs if x=="href"]    
            if len(a)>0:
                a=a[0]
                if "/?page=" in a:
                    self.maxPage=max(self.maxPage,int(a[7:]))
    def handle_data(self, data):
        if(self.insideTheTable and self.record and self.trn>1):
            
            if(not data.isnumeric()):
                self.fnames.append(data)
                self.cnt-=1
            self.record=self.cnt>0
        
    def handle_endtag(self,tag):
        if tag=="table":
            self.insideTheTable=False
        if tag=="td" or tag=="tr":
            self.record=False
            
def getNames():
    parser = MyHTMLParser()
    pn=0
    while pn<parser.maxPage:
        parser.insideTheTable=False;
        parser.trn=0;
        conn = http.client.HTTPSConnection("coinmarketcap.com")
        page="/?page={0}".format(pn+1)
        conn.request("GET", page)
        res = conn.getresponse()
        txt=""
        txt=str(res.read())

        conn.close()
        parser.feed(txt)
        pn+=1
#        print(pn)
        
    ret=[]
    for i in range(int(len(parser.fnames)/2)):
        ret.append((parser.fnames[i*2],parser.fnames[i*2+1]))
    return ret
names=getNames()
print(len(names))