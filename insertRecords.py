#!/usr/bin/env python3

from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
db = client.euterpeaedb
taxa_col = db.taxa
jsonfile = input('Enter json: ')

with open(jsonfile, 'r') as data:
    records = json.load(data)