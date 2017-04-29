#!/usr/bin/env python

import csv
import json
#import sys
#print(sys.argv[1:])
#file = input(file: )
input_file = input("Input file: ")
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
        'Taxonomic_status':'synomym',
        'Source':'source'
    }
    fields = fieldMap.keys()
    taxa =[]
    out_json.write('[\n')
    for row in reader:
        taxonomy ={}
        for field,value in row.items():
            #print(field,value)
            if field in fields and not value == "":
                taxonomy[fieldMap[field]] = value
                if field == 'Taxonomic_status':
                    if value == 'Accepted':
                        taxonomy[fieldMap[field]] = False
                    elif value =='Synonym':
                        taxonomy[fieldMap[field]] = True
                    else:
                        continue
                if field == 'Source':
                    taxonomy[fieldMap[field]] = value.split()
        fullname = [taxonomy['genus'],taxonomy['species'],taxonomy.get('infraTaxon',"")]
        out_splist.write("".join(fullname) + '\n')
        out_json.write(json.dumps(taxonomy,ensure_ascii=False)+',\n')
    out_json.write(']')                        
        #taxa.append(taxonomy)
    #json.dump(taxa,output)
    #output.write(json.dumps(taxa, sort_keys=False, indent=4, \
     #                       separators=(',', ': '),ensure_ascii=False))
