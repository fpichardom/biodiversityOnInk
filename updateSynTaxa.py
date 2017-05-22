#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:52:09 2017

@author: fritz
"""

import csv
import os.path
import sys

# Function Definition Start
def check_file(file):
    exists = True
    newfile = file
    while exists:
        if os.path.isfile(newfile):
            exists = False
        else:
            again = input('File %s does not exists\nDo yo want to enter a new file (y/n):'%newfile)
            if again in ['y','Y','yes','Yes']:
                newfile = input('Enter a new file name:' )
            else:                
                sys.exit('Program closed')
                
                
    return newfile


def clean_name(taxon):
    for i in ['subsp.','subsp','var.','var']:
        if i in taxon.split():
            taxonlist = taxon.split()
            taxonlist.remove(i)
            return "".join(taxonlist)
    return "".join(taxon.split())
# Function Definition End



input_file = check_file(input("Input file: "))

with open(input_file,'r') as csvfile:
    reader = csv.DictReader(csvfile,delimiter='\t')
    taxa= []
    for row in reader:
        if row['Taxonomic_status'] == 'Synonym':
            taxonomy ={}
            taxonomy['syn_fullname'] = clean_name(row['Name_submitted'])
            taxonomy['ac_fullname'] = clean_name(row['Accepted_name']) 
            taxa.append(taxonomy)