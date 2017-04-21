#!/usr/bin/env python

from pymongo import MongoClient
import json

client = MongoClient('localhost',27017)
db = client.euterpeaedb
collection = db.taxa
jsonfile = input('Enter json: ')

with open(jsonfile,'r') as data:
    taxa = json.load(data)
    for taxon in taxa:
        collection.insert_one(taxon)

        
        