#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 22:52:13 2017

@author: fritz
"""

from pymongo import MongoClient
#import json
import csv
#import datetime
import pprint


client = MongoClient('localhost', 27017)
db = client['gbifEuterpeae']
collection = db['records']


output = input("Output file name: " )
with open(output,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['#Fullname','Latitude','Longitude'])
    for record in collection.find({},{'properties.fullname':1,'geometry.coordinates':1,'_id':0}):
        fullname = record['properties']['fullname']
        latitude = record['geometry']['coordinates'][1]
        longitude = record['geometry']['coordinates'][0]
        todo =[fullname,latitude,longitude]
        writer.writerow(todo)
        pprint.pprint(record)
        
        
    