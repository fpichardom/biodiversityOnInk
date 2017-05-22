#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 19:02:44 2017

@author: fritz
"""

from pymongo import MongoClient
#import json
import datetime
#import pprint
import csv

client = MongoClient('localhost', 27017)
db = client['gbifEuterpeae']
collection = db['records']

def checkfloat(val):
    try:
        return float(val)
    except ValueError:
        return False
def checkint(val):
    try:
        return int(val)
    except ValueError:
        return False

#Load csv file
file = input('Enter file name: ')
database =input('Enter database name: ')
collection = input('Enter collection name: ')



with open(file,'r') as inputfile:
    reader = csv.DictReader(inputfile)
    #medio = list(reader)
    #termino =[]
    for i in reader:
        record = {'type':'Feature','properties':{},'geometry':{'type':'Point'}}
        
        for key,value in i.items():
            if key == 'decimalLongitude':
                lon = checkfloat(value)
            elif key == 'decimalLatitude':
                lat = checkfloat(value)
            elif key == 'year':
                year = checkint(value)
            elif key == 'month':
                month = checkint(value)
            elif key == 'day':
                day = checkint(value)
            else:
                if key != '' and value != '':
                    record['properties'][key] = value
        if lon != False and lat != False:
            record['geometry']['coordinates'] =[lon,lat]
        if year != False and month != False and day != False:
            record['eventDate'] = datetime.datetime(year,month,day)
        collection.insert_one(record)
        #termino.append(record)    
            
            
            
        '''           
            
            templat = None
            if key == 'decimalLongitude' and templat is None:
                record['geometry']['coordinates'].append(float(value))
            elif key == 'decimalLongitude' and templat is not None:
                record['geometry']['coordinates'].append(float(value))
                record['geometry']['coordinates'].append(templat)
            #elif key not in ('decimalLatitude','decimalLongitude'):
            #elif key != 'decimalLatitude' or key != 'decimalLongitude':
                #record['properties'][key] = value
            if key == 'decimalLatitude' and not record['geometry']['coordinates']:
                templat = float(value)
            elif key == 'decimalLatitude' and record['geometry']['coordinates']:
                record['geometry']['coordinates'].append(float(value))
            else:
                record['properties'][key] = value
        termino.append(record)
        '''
 
    '''      
for k,v  in medio[1].items():
    if k not in ('decimalLatitude','decimalLongitude'):
        print('no',k)
    else:
        print('si',k)
        '''