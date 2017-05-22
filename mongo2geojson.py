#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 10:10:22 2017

@author: fritz
"""

from pymongo import MongoClient
import json
#import datetime
#import pprint


client = MongoClient('localhost', 27017)
db = client['gbifEuterpeae']
collection = db['records']

output_json = input('Enter output name: ')

with open(output_json + '.json','w') as out_json:
    out_json.write('{ "type": "FeatureCollection", "features": [\n')
    first = True
    query = collection.find({'properties.fullname':'Prestoea tenuiramosa'},{'_id':0})
    for record in query:
        if first:
            out_json.write(json.dumps(record,ensure_ascii=False))
            first = False
        else:
            out_json.write(',\n' + json.dumps(record,ensure_ascii=False))        
       # out_json.write(json.dumps(record,ensure_ascii=False)+',\n')
    out_json.write(']}')     
    