#!/usr/bin/env python

from pymongo import MongoClient
import json
import os.path
import sys

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


client = MongoClient('localhost', 27017)
db = client['euterpeaedb']
collection = db['taxa']

jsonfile = check_file(input('Enter json: '))

with open(jsonfile, 'r') as data:
    taxa = json.load(data)
    for taxon in taxa:
        try:
            collection.insert_one(taxon)
        except:
            fullname = " ".join([taxon['genus'],taxon['species'],taxon.get('infraTaxon',"")])
            print("%s skipped!"%fullname)
    #collection.insert_many(taxa, ordered=False)
        