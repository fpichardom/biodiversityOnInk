#!/usr/bin/env python

from pymongo import MongoClient
import json
import datetime
import pprint
import os.path
import sys

# Start functions definitions

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

# End function definitions

#Load json

jsonfile = check_file(input('Enter json: '))

# Database connection

client = MongoClient('localhost', 27017)
database = client[input('Enter database name: ')]
collection = database[input('Enter collection name: ')]


# General script


with open(jsonfile, 'r') as data:
    publications = json.load(data)
    for publication in publications:
        publication['date'] = datetime.datetime.strptime(publication['date'],"%Y-%m-%d")
        publication['ID'] = publication['author'][0].split(',')[0].lower()+':'+ \
        str(publication['date'].year)+':'+ publication['title'][0:4].lower()        
        find_query = collection.find_one({'ID':publication['ID']},{'_id':0, 'title':1, 'author':1, 'date':1,'ID':1})
        if find_query is None:
            collection.insert_one(publication)
        else:
            print('\nDuplicate bibtex key!!!\n')
            pprint.pprint(find_query)
            print('\n\n')
            pprint.pprint(publication)
            add = input('Add current entry anyway (y/n): ')
            if add in ['y','Y','Yes','yes']:
                origID = publication['ID']
                while collection.find_one({'ID':publication['ID']}):
                    suf = input('Add suffix to key: ')
                    publication['ID'] = origID+':'+suf
                print('New key ID accepted')
                collection.insert_one(publication)
            else:
                print('Entry Skipped!')
                
            
            