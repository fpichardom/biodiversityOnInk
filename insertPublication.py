#!/usr/bin/env python

from pymongo import MongoClient
import json
import datetime
import pprint
import os
import os.path
import sys
from unidecode import unidecode
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


def clean_date(date):
    parts = date.split('/')
    if len(parts) == 3:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        return datetime.datetime(year,month,day,12,0,0)
    else:
        return date
# End function definitions

os.chdir(input("Enter files path: "))

#Load json

jsonfile = check_file(input('Enter json: '))

# Database connection

client = MongoClient('localhost', 27017)
database = client[input('Enter database name: ')]
collection = database[input('Enter collection name: ')]
cataloger = input('Enter cataloger name: ') 
utcnow = datetime.datetime.utcnow()
# General script


with open(jsonfile, 'r') as data:
    publications = json.load(data)
    for publication in publications:
        publication['catalogDate'] = utcnow
        publication['cataloger'] = cataloger
        publication['date'] = clean_date(publication['date'])
        publication['ID'] = unidecode(publication['author'][0].split(',')[0].lower())+':'+ \
        str(publication['date'].year)+':'+ publication['title'][0:4].lower().strip()     
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
                    for letter in ['a','b','c','d','e','f','g','h','i']:
                        suf = letter
                        publication['ID'] = origID + ':' + suf
                print('New key ID accepted',publication['ID'])
                collection.insert_one(publication)
            else:
                print('Entry Skipped!')
                
            
            