#!/usr/bin/env python

from pymongo import MongoClient
import json
import os.path
import sys
import os
import datetime


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

#Input files
jsonfile = check_file(input('Enter json: '))

#Database Connection
client = MongoClient('localhost', 27017)
database = client[input('Enter database name: ')]
collection = database[input('Enter collection name: ')]
cataloger = input('Enter cataloger name: ') 
utcnow = datetime.datetime.utcnow()

with open(jsonfile, 'r') as data:
    taxa = json.load(data)
    for taxon in taxa:
        try:
            taxon['catalogDate'] = utcnow
            taxon['cataloger'] = cataloger
            collection.insert_one(taxon)
            fullname = " ".join([taxon['genus'],taxon['species'],taxon.get('infraTaxon',"")])
            print("%s added!"%fullname)
        except:
            fullname = " ".join([taxon['genus'],taxon['species'],taxon.get('infraTaxon',"")])
            print("%s skipped!"%fullname)
    #collection.insert_many(taxa, ordered=False)
        