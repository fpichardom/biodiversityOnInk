#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 11:03:35 2017

@author: fritz
"""

from pymongo import MongoClient # allow to connect to database
from bson.objectid import ObjectId # handles objectIds
import json
from bson.son import SON # for sort operations
import pprint # allow better printing
import datetime
client = MongoClient('localhost', 27017) # make server connection
db = client.euterpeaedb # connect to database
taxacol = db.taxa #access taxa collection
recordcol = db.record
datecol = db.datecol
fullname_pipeline = [
        
        { "$project": {
                "fullname": { "$concat": ["$genus",
                                          "$species",
                                          { "$ifNull": [ "$InfraTaxon", "" ] }
                                         ]
                            },
                "include":"to_include"
                      }
        }
]

for i in taxacol.aggregate(fullname_pipeline):
    pprint.pprint(i)
'''
jsonfile = input('Enter json: ')

with open(jsonfile, 'r') as data:
    taxa = json.load(data)
    collection.insert_many(taxa, ordered=False)
    
    { $ifNull: [ "$InfraTaxon", "" ] }
'''
datetime.datetime()