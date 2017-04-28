#!/usr/bin/env python3
import argparse as ap

a =[{"country": "Dominican Republic",
    "geoLoc":{"type":"Point", "coordinates":["70 20 30 W","42 15 23.245 N"]}
    },
    { "country": "Canada",
    "geoLoc":{"type":"Point", "coordinates":[-80.96547,50.12687]}
    },
    { "country": "Canada"}
]
# d = {'key1': 'value1', 'key2': 'value2'}

# n = ap.Namespace(**a)


for i in range(len(a)):
    if a[i].get('geoLoc',0):
        print("is there")
        if type(a[i]['geoLoc']['coordinates'][0]) == float:
            print("good")
        else:
            print("need parse")
            if len(a[i]['geoLoc']['coordinates'][0].split(' ')) == 4:
               newcor = []
               for cor in a[0]['geoLoc']['coordinates']:
                   print(cor.split(' '))
                   parse = cor.split(' ')
                   dd = float(parse[0]) + float(parse[1])/60 + float(parse[2])/(60*60)
                   if parse[3] == 'S' or parse[3] == 'W':
                       dd *= -1
                   newcor.append(dd)
               a[i]['geoLoc']['coordinates'] = newcor
    else:
        print("not there")
        