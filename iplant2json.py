#!/usr/bin/env python

import csv
import json
import sys
print(sys.argv[1:])
#file = input(file: )
with open(sys.argv[1],'r') as csvfile,open(sys.argv[2],'w') as output:
    reader = csv.DictReader(csvfile,delimiter='\t')
    title = reader.fieldnames
    #lista = list(reader)    
    #fieldMap fielname as in document and value as newfieldname
    fieldMap = {
        'Name_matched_accepted_family':'family',
        'Genus_matched':'genus',
        'Specific_epithet_matched':'species',
        'Infraspecific_rank':'InfraRank',
        'Infraspecific_epithet_matched':'InfraTaxon',
	    'Name_matched_author':'taxonAuthor',
        'Taxonomic_status':'synomym'
    }
    fields = fieldMap.keys()
    taxa =[]
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
                            
        taxa.append(taxonomy)
    #json.dump(taxa,output)
    output.write(json.dumps(taxa, sort_keys=False, indent=4, separators=(',', ': '),ensure_ascii=False))
