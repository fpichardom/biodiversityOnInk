#!/usr/bin/env python

import csv
import json
import sys
import os.path
#print(sys.argv[1:])
#file = input(file: )

def clean_syn(value):    
    if value == 'Accepted':
        return False
    elif value =='Synonym':
        return True
    else:
        return value
    
def clean_source(value):
    return value.split(';')
    
def clean_fullname(value):
    p = value.split()        
    for i in ['subsp.','subsp','var.','var']:
        if i in p:
            p = value.split()
            return {'genus':p[0],'species':p[1],'infraRank':p[2],'infraTaxon':p[3]}
    return {'genus':p[0],'species':p[1]}
    

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
'''
def check_first_write(taxonomy,first):
    if first:
        out_json.write(json.dumps(taxonomy,ensure_ascii=False))
    else:
        out_json.write(',\n'+ json.dumps(taxonomy,ensure_ascii=False))
'''

input_file = check_file(input("Input file: "))
output_json = input("Output json file: ")
output_splist = input("Output species list: ")

with open(input_file,'r') as csvfile, open(output_json + '.json','w') as out_json, \
    open(output_splist + '.txt','w') as out_splist:
    reader = csv.DictReader(csvfile,delimiter='\t')
    title = reader.fieldnames
    #lista = list(reader)    
    #fieldMap fielname as in document and value as newfieldname
    fieldMap = {
        'Name_matched_accepted_family':'family',
        'Genus_matched':'genus',
        'Specific_epithet_matched':'species',
        'Infraspecific_rank':'infraRank',
        'Infraspecific_epithet_matched':'infraTaxon',
	    'Name_matched_author':'taxonAuthor',
        'Taxonomic_status':'synonym',
        'Source':'source'
    }
    fields = fieldMap.keys()
    taxa =[]
    out_json.write('[\n')
    first = True
    for row in reader:       
        if row['Taxonomic_status'] == 'Synonym':
            taxonomy ={}
            taxonomy['family'] = row['Accepted_name_family']
            taxonomy.update(clean_fullname(row['Accepted_name']))
            taxonomy['taxonAuthor'] = row['Accepted_name_author']
            taxonomy['synonym'] = False
            taxonomy['source'] = clean_source(row['Source'])
            if first:
                out_json.write(json.dumps(taxonomy,ensure_ascii=False))
                first = False
            else:
                out_json.write(',\n'+ json.dumps(taxonomy,ensure_ascii=False))
            
            #out_json.write(json.dumps(taxonomy,ensure_ascii=False)+',\n')
        taxonomy ={}
        for field,value in row.items():
            #print(field,value)
            if field in fields and not value == "":
                taxonomy[fieldMap[field]] = value
                if field == 'Taxonomic_status':
                    taxonomy[fieldMap[field]] = clean_syn(value)
                if field == 'Source':
                    taxonomy[fieldMap[field]] = clean_source(value)
        fullname = [taxonomy['genus'],taxonomy['species'],taxonomy.get('infraTaxon',"")]
        out_splist.write("".join(fullname) + '\n')
        if first:
            out_json.write(json.dumps(taxonomy,ensure_ascii=False))
            first = False
        else:
            out_json.write(',\n'+ json.dumps(taxonomy,ensure_ascii=False))
        #out_json.write(json.dumps(taxonomy,ensure_ascii=False)+',\n')
    out_json.write('\n]')                        
        #taxa.append(taxonomy)
    #json.dump(taxa,output)
    #output.write(json.dumps(taxa, sort_keys=False, indent=4, \
     #                       separators=(',', ': '),ensure_ascii=False))
