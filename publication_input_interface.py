#!/usr/bin/env python

import publications_mongo
from general import check_file,connect_db

# Constant definitions

DBNAME = input('Enter database name: ')
PUBCOLNAME = input('Enter publications collection name: ')
#CATALOGER = input('Enter cataloger name: ')
##Load json file
JSONFILE = check_file(input('Enter json: '))

# Database connection
PUBCOL = connect_db(DBNAME,PUBCOLNAME)
publications_mongo.pub_insert(JSONFILE,PUBCOL)
