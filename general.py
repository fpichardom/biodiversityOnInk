#!/usr/bin/env python

import os.path
import sys
import os
import datetime
from pymongo import MongoClient

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

def clean_date(date):
    parts = date.split('/')
    if len(parts) == 3:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        return datetime.datetime(year,month,day,13,0,0) # set time of the daty to 13:00 hours by default
    else:
        return date


## Database connection

def connect_db(database, collection, client=MongoClient('localhost', 27017)):
    '''
    Manage connection to the mongo server and database
    '''
    dbase = client[database]
    col = dbase[collection]
    return col

def fixcoord(dictio):
    """
    Parse strings formated in DM or DMS to DD
    """
    newcor =[]
    for cor in dictio['geometry']['coordinates']:
        parse = cor.split(' ')
        if len(parse) == 3:
            dd = float(parse[0]) + float(parse[1])/60
            if parse[2] == 'S' or parse[2] == 'W':
                dd *= -1
        elif len(parse) == 4:
            dd = float(parse[0]) + float(parse[1])/60 + float(parse[2])/(60*60)
            if parse[3] == 'S' or parse[3] == 'W':
                dd *= -1
        newcor.append(dd)
    return newcor

def checkfloat(val):
    """
    Check if a string can be converted into float
    """
    try:
        float(val)
        return True
    except ValueError:
        return False