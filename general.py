#!/usr/bin/env python

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
