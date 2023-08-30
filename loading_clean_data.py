#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 12:00:48 2021

@author: shoale
"""

import pandas as pd


data_2017 = pd.read_csv("playerdata2017.csv")
data_2018 = pd.read_csv("playerdata2018.csv")
data_2019 = pd.read_csv("playerdata2019.csv")

data_2017 = data_2017.drop(["Unnamed: 0"], axis=1)
data_2018 = data_2018.drop(["Unnamed: 0"], axis=1)
data_2019 = data_2019.drop(["Unnamed: 0"], axis=1)

data_2017 = data_2017.rename(columns={"0":"Player", "1":"Market Value", "2":"Position", "3":"Team"})
data_2018 = data_2018.rename(columns={"0":"Player", "1":"Market Value", "2":"Position", "3":"Team"})
data_2019 = data_2019.rename(columns={"0":"Player", "1":"Market Value", "2":"Position", "3":"Team"})


