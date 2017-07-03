#!/usr/bin/env python

#import statements
import os.path
import sys
import os
import taxa_mongo
from general import check_file, connect_db

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

TAXACOL = connect_db(DBNAME, TAXACOLNAME)
VIEW = connect_db(DBNAME, VIEWNAME)
# Main program run stage

taxa_mongo.run_body(I_FILE, TAXACOL, VIEW, FIELD_MAP)
