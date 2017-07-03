#!/usr/bin/env python

from general import check_file,clean_date,connect_db


# Constant definitions

DBNAME = input('Enter database name: ')
PUBCOLNAME = input('Enter publications collection name: ')
#CATALOGER = input('Enter cataloger name: ')
##Load json file
JSONFILE = check_file(input('Enter json: '))

# Database connection
PUBCOL = connect_db(DBNAME,PUBCOLNAME)
