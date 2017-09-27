#!/usr/bin/env python3
"""
Insert records into mongodb
"""

import json
from pymongo import MongoClient
import datetime
import os.path
import sys
import os


def find_pubid(ukey,database):
    keep = True
    while keep:
        query = database['publications'].find_one({'ID':ukey},{'_id':1})
        if query is None:
            ukey = input('Try again: ')
        else:
            keep = False               
    return query['_id']

def find_taxonid(file,database):    
    with open(file,'r') as spfile :
        lista = spfile.read().split('\n')
        query = database['fullname_view'].aggregate( [
		{ "$match": { "fullname": { "$in": lista } } },
		{ "$project": { "todo" : "include", "_id" : 1 } },
		{ "$group": { "_id": "$todo", "taxonId": { "$addToSet": "$_id" } } } ] )
    
    for item in query:
        taxonId = item['taxonId']
    return taxonId

def clean_date(date):
    parts = date.split('/')
    if len(parts) == 3:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
    return datetime.datetime(year,month,day,12,0,0)
        
def check_file(file):
    exists = True
    newfile = file
    while exists:
        if os.path.isfile(newfile):
            exists = False
        else:
            again = input('File %s does not exists\nDo yo want to enter a new file (y/n):'%newfile)
            if again in ['y','Y','yes','Yes']:
                newfile = input('Enter a new file name:' )
            else:                
                sys.exit('Program closed')
                
                
    return newfile
                

os.chdir(input("Enter files path: "))

# Enter external files  

jsonfile = check_file(input('Enter json: '))
taxonfile = check_file(input('Enter taxon file: '))

# Database connection

client = MongoClient('localhost', 27017)
database = client[input('Enter database name: ')]
collection = database[input('Enter collection name: ')]

# General info for all records

cataloger = input('Enter cataloger name: ') 
pubid = find_pubid(input('Enter publication key: '),database)
taxonid = find_taxonid(taxonfile,database)
utcnow = datetime.datetime.utcnow()
print('Starting entry process')


# Load data and run program

with open(jsonfile, 'r') as data:
    records = json.load(data)
    count = 0
    for record in records:
        try:
            record['catalogDate'] = utcnow
            record['cataloger'] = cataloger
            record['publicationId'] = pubid
            record['TaxonId'] = taxonid
            if record.get('geometry', 0):
                if not general.checkfloat(record['geometry']['coordinates'][0]):
                    record['geometry']['coordinates'] = general.fixcoord(record)
            if record.get('startDateTime', 0):
                record['startDateTime'] = clean_date(record['startDateTime'])
            if record.get('endDateTime', 0):
                record['endDateTime'] = clean_date(record['endDateTime'])
            count += 1
            print('Record %s proccessed'%count)
            #collection.insert_one(record) # records inserted as processed
        except:
            print('Error found no record inserted')
    collection.insert_many(records) # records inserted at the end of the process
    print('All records successfully uploaded')





    