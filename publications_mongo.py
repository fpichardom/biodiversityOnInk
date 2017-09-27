#!/usr/bin/env python


import json
import datetime
import pprint
from unidecode import unidecode
from general import clean_date

# Start functions definitions


def pub_insert(jsonfile, collection, cataloger='Pichardo-Marcano, Fritz'):
    """
    Cleans the publication file and insert it to the database
    """
    with open(jsonfile, 'r') as data:
        publications = json.load(data)
        for publication in publications:
            publication['catalogDate'] = datetime.datetime.utcnow()
            publication['cataloger'] = cataloger
            publication['date'] = clean_date(publication['date'])
            publication['bibId'] = unidecode(publication['author'][0].split(',')[0].lower())+'-'+\
            str(publication['date'].year)+'-'+\
            publication['title'][0:4].lower().strip()
            find_query = collection.find_one({'bibId':publication['bibId']}, {'_id':0, 'title':1, 'author':1, 'date':1,'bibId':1})
            if find_query is None:
                collection.insert_one(publication)
            else:
                print('\nDuplicate bibtex key!!!\n')
                pprint.pprint(find_query)
                print('\n\n')
                pprint.pprint(publication)
                add = input('Add current entry anyway (y/n): ')
                if add in ['y','Y','Yes','yes']:
                    orig_id = publication['bibId']
                    while collection.find_one({'bibId':publication['bibId']}):
                        for letter in ['a','b','c','d','e','f','g','h','i']:
                            suf = letter
                            publication['bibId'] = orig_id + '-' + suf
                    print('New key ID accepted',publication['bibId'])
                    collection.insert_one(publication)
                else:
                    print('Entry Skipped')
