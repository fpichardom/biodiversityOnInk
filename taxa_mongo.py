#!/usr/bin/env python
'''
Provides code to parse a csv file obtained from the taxonomic name resolution system
'''
# import modules stage

import csv
import datetime
from pymongo import MongoClient
# function declaration stage

## Database connection

def connect_db(database, collection, client=MongoClient('localhost', 27017)):
    '''
    Manage connection to the mongo server and database
    '''
    dbase = client[database]
    col = dbase[collection]
    return col

## Accessory functions

def fullname_insert(value):
    '''
    Parse a string with the fullname of a taxon into its separate components
    '''
    parse = value.split()
    if len(parse) == 2:
        return {'genus':parse[0], 'specificEpithet':parse[1]}
    if len(parse) == 4:
        return {'genus':parse[0], 'specificEpithet':parse[1], \
        'verbatimTaxonRank':parse[2], 'infraspecificEpithet':parse[3]}
    else:
        return {'genus':parse[0]}

def fullname_update(taxon):
    taxonlist = taxon.split()       
    for i in ['subsp.','subsp','var.','var']:
        if i in taxonlist:            
            taxonlist.remove(i)
            return "".join(taxonlist)
    return "".join(taxonlist)



def insert_taxa(taxon, collection, cataloger='Pichardo-Marcano, Fritz'):
    '''
    Insert a new taxon to the mongodb database
    '''
    try:
        taxon['catalogDate'] = datetime.datetime.utcnow()
        taxon['cataloger'] = cataloger
        collection.insert_one(taxon)
        fullname = " ".join([taxon['genus'], taxon.get('specificEpithet', ""), \
        taxon.get('infraspecificEpithet', "")])
        print("%s added!"%fullname)
    except:
        fullname = " ".join([taxon['genus'], taxon.get('specificEpithet', ""),\
        taxon.get('infraspecificEpithet', "")])
        print("%s skipped!"%fullname)


def id_search(fullname, collection):
    query = collection.find_one({ "fullname": fullname },{"_id":1})
    return query['_id']


## Main taxa parse and insert

def run_body(input_file, insert_collection, field_map, output_splist='splist.txt'):
    '''
    Main program for parsing and inserting taxon data into the mongodb database
    '''
    with open(input_file, 'r') as csvfile, open(output_splist + '.txt', 'w') as splist:
        general_fields = field_map.keys()
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            if row['Taxonomic_status'] == 'Synonym':
                taxonomy = {}
                taxonomy['family'] = row['Accepted_name_family']
                taxonomy['scientificNameAuthorship'] = row['Accepted_name_author']
                taxonomy['taxonRank'] = row['Accepted_name_rank']
                taxonomy['nameAccordingTo'] = row['Source'].split(';')
                taxonomy['taxonomicStatus'] = "accepted"
                taxonomy.update(fullname_insert(row['Accepted_name']))
                insert_taxa(taxonomy, insert_collection)
            taxonomy = {}
            for field, value in row.items():
                if field in general_fields and not value == "":
                    taxonomy[field_map[field]] = value
                    if field == 'Taxonomic_status':
                        taxonomy[field_map[field]] = value.lower()
                    if field == 'Source':
                        taxonomy[field_map[field]] = value.split(';')
            insert_taxa(taxonomy, insert_collection)
            fullname = "".join([taxonomy['genus'], taxonomy.get('specificEpithet', ""),\
            taxonomy.get('infraspecificEpithet', "")])
            splist.write(fullname + '\n')

## Main parse and update synonyms


def update_synonym(input_file):
    with open(input_file,'r') as csvfile:
    reader = csv.DictReader(csvfile,delimiter='\t')
    #taxai= []
    for row in reader:
        if row['Taxonomic_status'] == 'Synonym':
            syn = id_search(fullname_update(row['Name_matched']))
            acc = id_search(fullname_update(row['Accepted_name']))
            collection.update_one({"_id":syn},{"$set":{"acceptedNameUsage": acc}})
            #taxonomy =[syn,acc]
            #taxai.append(taxonomy)


