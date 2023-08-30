#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 18:27:25 2021

@author: shoale
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import json

base_url="https://www.transfermarkt.co.uk"
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    

 #takes years in STR (2020,2019, etc)
#takes leauge accorinng to TransferMarkt format
 #English Premier = GB1
 #Spain La Liga = ES1
 #Italt Serie A = IT1
 #Germany BundesLiga = L1
 #France Ligue1 = FR1

        
def get_data(leagues,years): #Returns a single DF with TransferMarkt ID, name, position, team, and dict of injuries 
    
    #Collect the list of all teams and generate links from the teams list
    page = 'https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/'+leagues+'/plus/?saison_id='+str(years)
    tree = requests.get(page, headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    teams = soup.find("table", class_="items").find("tbody")
    link=teams.find_all("a", class_="vereinprofil_tooltip")
    links=link[::3]
    teamlist=[]
    linklist=[]
    
    for i in range(len(teamlist)):
        teamlist.append(re.search("\/(.*?)\/",links[i]["href"])[1])
        linklist.append(base_url+links[i]["href"])

    output=pd.DataFrame() # Create empty df 

    for j in range(len(linklist)): # Append data of each team to the output DF
        soup1=BeautifulSoup(requests.get(linklist[j], headers = headers).content, 'html.parser')
        playertable=soup1.find("table", class_="items") #Player list
        playertable_inj=soup1.findAll(class_="spielprofil_tooltip")[::2] #Player list (sepeartely for injury)
        #Injury list comes from another table on a separate URL
        ids=[]
        injury_list=[]

        for player in playertable_inj:
            link_maker=str(player).split(" ")[2].split("/")
            name=link_maker[1]
            id1=link_maker[4][:-1]
            ids.append(id1)
            link_made="https://www.transfermarkt.co.uk/"+name+"/verletzungen/spieler/"+id1
            soup_inj=BeautifulSoup(requests.get(link_made, headers = headers).content, 'html.parser')
            
            inja = soup_inj.find("table", class_="items") #Check if there is injury data for the player
            if inja is not None:
                injuries=inja.find("tbody")
                duration=[int(re.findall("\d+", x.text)[0]) for x in injuries.find_all("td",class_="rechts")[::2]]
                inj_type=[x.text for x in injuries.find_all("td",class_="hauptlink")[::2]]
                seasons=[x.text for x in injuries.find_all("td",class_="zentriert")[::3]]
                began=[x.text for x in injuries.find_all("td",class_="zentriert")[1::3]]
                end=[x.text for x in injuries.find_all("td",class_="zentriert")[2::3]]
                details = ["injury_type", "season", "duration", "began", "end"]

                inj = {}
                for n in range(len(inj_type)):
                    name = "injury " + str(n)
                    detail_list = [inj_type[n],seasons[n],duration[n],began[n],end[n]]
                    inj_data = dict(zip(details, detail_list))
                    inj[name] = inj_data
                injury_data = {"injury_detail": [inj]}

                injury_list.append(injury_data["injury_detail"])
            else:
                injury_list.append("")
        
        rows = playertable.find_all('td',class_="posrela")
        players=[x.find(class_="spielprofil_tooltip").text for x in rows]
        positions=[x.find_all("td")[-1].text for x in rows]
        team=[teamlist[j]]*len(players)
        data=pd.DataFrame(list(zip(ids,players,positions,team,injury_list)))

        output=output.append(data)

    return output



get_data("GB1", 2020)