#!/usr/bin/env python3
"""
Insert records into mongodb
"""

import json
from pymongo import MongoClient
import datetime

def fixcoord(dictio):
    """
    Parse strings formated in DM or DMS to DD
    """
    newcor =[]
    for cor in dictio['geometry']['coordinates']:
        parse = cor.split(' ')
        if len(parse) == 3:
            dd = float(parse[0]) + float(parse[1])/60
            if parse[2] == 'S' or parse[2] == 'W':
                dd *= -1
        elif len(parse) == 4:
            dd = float(parse[0]) + float(parse[1])/60 + float(parse[2])/(60*60)
            if parse[3] == 'S' or parse[3] == 'W':
                dd *= -1
        newcor.append(dd)
    return newcor

def checkfloat(val):
    """
    Check if a string can be converted into float
    """
    try:
        return float(val)
    except ValueError:
        return False

def find_pubid(ukey,database):
    keep = True
    while keep:
        query = database['publications'].find_one({'ID':ukey},{'_id':1})
        if query is None:
            ukey = input('Try again: ')
        else:
            keep = False               
    return query['_id']

def find_taxonid(file):    
    with open(file,'r') as spfile :
        lista = spfile.read().split('\n')
        query = database['fullname_view'].aggregate( [
		{ "$match": { "fullname": { "$in": lista } } },
		{ "$project": { "todo" : "include", "_id" : 1 } },
		{ "$group": { "_id": "$todo", "taxonId": { "$addToSet": "$_id" } } } ] )
    
    for item in query:
        taxonId = item['taxonId']
    return taxonId


jsonfile = input('Enter json: ')
db = input('Enter database name: ')
col = input('Enter collection name: ')
pubid = input('Enter publication key: ')
taxonfile = input('Enter taxon file: ')
client = MongoClient('localhost', 27017)
database = client[db]
collection = database[col]


with open(jsonfile, 'r') as data:
    records = json.load(data)
    #pubid = find_pubid(pubid)
    for record in records:
        record['publicationId'] = find_pubid(pubid,database)
        record['TaxonId'] = find_taxonid(taxonfile)
        if record.get('geometry', 0):
            if checkfloat(record['geometry']['coordinates'][0]):
                continue
            else:
                record['geometry']['coordinates'] = fixcoord(record)
        if record.get('startDateTime', 0):
            record['startDateTime'] = datetime.datetime.strptime(record['startDateTime'],"%Y-%m-%d")
        if record.get('endDateTime', 0):
            record['endDateTime'] = datetime.datetime.strptime(record['startDateTime'],"%Y-%m-%d")
        #collection.insert_one(record)






    