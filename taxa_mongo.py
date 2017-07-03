#!/usr/bin/env python
'''
Provides code to parse a csv file obtained from the taxonomic name resolution system
'''
# import modules stage
import csv
import datetime
from pymongo import MongoClient

# function declaration stage



## Accessory functions

def fullname_parse(value):
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
    '''
    Search for the id based on a concatenated fullname
    '''
    query = collection.find_one({"fullname": fullname}, {"_id":1})
    return query['_id']

def update_synonym(synonym, accepted, update_collection, lookup_collection):
    '''
    Update synonyms
    '''
    syn = id_search(synonym, lookup_collection)
    acc = id_search(accepted, lookup_collection)
    update_collection.update_one({"_id":syn}, {"$set":{"acceptedNameUsage": acc}})

## Main taxa parse and insert

def run_body(input_file, insert_collection, lookup_collection, field_map,\
output_splist='splist'):
    '''
    Main program for parsing and inserting taxon data into the mongodb database
    '''
    with open(input_file, 'r') as csvfile, open(output_splist + '.txt', 'w') as splist:
        general_fields = field_map.keys()
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            acc = None
            if row['Taxonomic_status'] == 'Synonym':
                taxonomy = {}
                taxonomy['family'] = row['Accepted_name_family']
                taxonomy['scientificNameAuthorship'] = row['Accepted_name_author']
                taxonomy['taxonRank'] = row['Accepted_name_rank']
                taxonomy['nameAccordingTo'] = row['Source'].split(';')
                taxonomy['taxonomicStatus'] = "accepted"
                taxonomy.update(fullname_parse(row['Accepted_name']))
                insert_taxa(taxonomy, insert_collection)
                acc = "".join([taxonomy['genus'], taxonomy.get('specificEpithet', ""),\
            taxonomy.get('infraspecificEpithet', "")])
            taxonomy = {}
            for field, value in row.items():
                if field in general_fields and not value == "":
                    taxonomy[field_map[field]] = value
                    if field == 'Taxonomic_status':
                        taxonomy[field_map[field]] = value.lower()
                    if field == 'Source':
                        taxonomy[field_map[field]] = value.split(';')
            insert_taxa(taxonomy, insert_collection)
            syn = "".join([taxonomy['genus'], taxonomy.get('specificEpithet', ""),\
            taxonomy.get('infraspecificEpithet', "")])
            splist.write(syn + '\n')
            if acc:
                update_synonym(syn, acc, insert_collection, lookup_collection)
