#!/usr/bin/env python

import os.path
import sys
import os
import taxa_mongo

# Function declaration

def check_file(file):
    '''
    Check if file exists in a specific directory
    '''
    exists = True
    newfile = file
    os.chdir(input("Enter files path: "))
    while exists:
        if os.path.isfile(newfile):
            exists = False
        else:
            again = input('File %s does not exists\nDo yo want to enter a new file (y/n):'%newfile)
            if again in ['y', 'Y', 'yes', 'Yes']:
                newfile = input('Enter a new file name:')
            else:
                sys.exit('Program closed')
    return newfile

# Constant declaration stage

I_FILE = check_file(input("Input file: "))
DBNAME = input('Enter database name: ')
TAXACOLNAME = input('Enter taxa collection name: ')
VIEWNAME = input('Enter view collection name: ')
#CATALOGER = input('Enter cataloger name: ')
#SPLIST = input("Output species list: ")

## field_map key as in document and value as in database

FIELD_MAP = {
    'Name_matched_accepted_family':'family',
    'Genus_matched':'genus',
    'Specific_epithet_matched':'specificEpithet',
    'Name_matched_rank':'taxonRank',
    'Infraspecific_rank':'verbatimtaxonRank',
    'Infraspecific_epithet_matched':'infraspecificEpithet',
    'Name_matched_author':'scientificNameAuthorship',
    'Taxonomic_status':'taxonomicStatus',
    'Source':'nameAccordingTo'
}

# Database connection stage

TAXACOL = taxa_mongo.connect_db(DBNAME, TAXACOLNAME)
VIEW = taxa_mongo.connect_db(DBNAME, VIEWNAME)
# Main program run stage

taxa_mongo.run_body(I_FILE, TAXACOL, VIEW, FIELD_MAP)
