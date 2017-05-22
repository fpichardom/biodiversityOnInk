#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:52:09 2017

@author: fritz
"""

import csv


def clean_name(taxon):
    if 2 <= len(taxon.split()) <= 3:
        return taxon.replace(' ','')
    elif len(taxon.split()) == 4:
        
        
    
    
    
    
input_file = input("Input file: ")

with open(input_file,'r') as csvfile:
    reader = csv.DictReader(csvfile,delimiter='\t')
    fieldMap = {
        'Name_submitted':'syn_fullname',
        'Accepted_name':'ac_fullname',
    }
    fields = fieldMap.keys()
    for row in reader:
        if row['Taxonomic_status'] == Synonym
        taxonomy ={}
        taxonomy['syn_fullname'] = 
        for field,value in row.items():
            #print(field,value)
            if field in fields and not value == "":