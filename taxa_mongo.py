#!/usr/bin/env python

# import modules stage

import csv
import datetime
from pymongo import MongoClient
# function declaration stage


def connect_db(database, collection, client=MongoClient('localhost', 27017)):
    db = client[database]
    col = db[collection]
    return col

def clean_fullname(value):
    parse = value.split()
    if len(parse) == 2:
        return {'genus':parse[0], 'specificEpithet':parse[1]}
    if len(parse) == 4:
        return {'genus':parse[0], 'specificEpithet':parse[1], \
        'verbatimTaxonRank':parse[2], 'infraspecificEpithet':parse[3]}
    else:
        return {'genus':parse[0]}
'''
    for i in ['subsp.','subsp','var.','var']:
        if i in p:
            p = value.split()
            return {'genus':p[0],'species':p[1],'infraRank':p[2],'infraTaxon':p[3]}
    return {'genus':p[0],'specificEpithet':p[1]}
'''


def insert_taxa(taxon, collection, cataloger='Pichardo-Marcano, Fritz'):
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




def run_body(input_file, collection, field_map, output_splist='splist.txt'):
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
                taxonomy.update(clean_fullname(row['Accepted_name']))
                insert_taxa(taxonomy, collection)
            taxonomy = {}
            for field, value in row.items():
                if field in general_fields and not value == "":
                    taxonomy[field_map[field]] = value
                    if field == 'Taxonomic_status':
                        taxonomy[field_map[field]] = value.lower()
                    if field == 'Source':
                        taxonomy[field_map[field]] = value.split(';')
            insert_taxa(taxonomy, collection)
            fullname = "".join([taxonomy['genus'], taxonomy.get('specificEpithet', ""),\
            taxonomy.get('infraspecificEpithet', "")])
            splist.write(fullname + '\n')