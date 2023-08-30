#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 11:42:07 2021

@author: shoale
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

base_url="https://www.transfermarkt.co.uk"
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    

def numconvert(num):
    num=num[1:]
    if len(num)>1:
        if num[-1]=='m':
            return float(num[:-1])*1000000
        elif num[-1]!='m':
            return float(num[:-3])*1000
    else:
        print(num)
        
        
for years in [2016,2017,2018]:
    
    page = 'https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id='+str(years)
    tree = requests.get(page, headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    teams = soup.find("table", class_="items").find("tbody")
    link=teams.find_all("a", class_="vereinprofil_tooltip")
    links=link[::3]

    teamlist=[]
    linklist=[]

    for i in range(0,20):
        teamlist.append(re.search("\/(.*?)\/",links[i]["href"])[1])
        linklist.append(base_url+links[i]["href"])

    output=pd.DataFrame()

    for j in range(0,20):
        soup1=BeautifulSoup(requests.get(linklist[j], headers = headers).content, 'html.parser')
        playertable=soup1.find("table", class_="items")
        marketvalues=[numconvert(x.text.replace(u'\xa0', u'')) if x.text.replace(u'\xa0', u'')!='' else 0 for x in playertable.find_all(class_="rechts hauptlink")]
        rows = playertable.find_all('td',class_="posrela")
        players=[x.find(class_="spielprofil_tooltip").text for x in rows]
        positions=[x.find_all("td")[-1].text for x in rows]
        team=[teamlist[j]]*len(players)
        data=pd.DataFrame(list(zip(players,marketvalues,positions,team)))
        output=output.append(data)
    
    output.to_csv(r'playerdata'+str(years+1)+'.csv')