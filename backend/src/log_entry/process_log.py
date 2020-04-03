#!/bin/python3

#Nginx server_log to psql DB

import requests
import urllib
import json
import psycopg2
from psycopg2 import sql
import pandas as pd

def process_log(file):
    #read the nginx log file
    
    '''if request.method == "POST":
        file = request.files['file']
    file = request.files'''

        #GET DB CREDS
    with open('/home/extralime/Desktop/flask-test/uploads/db-creds.json') as cred_data:
        info = json.load(cred_data)
        DBNAME = info['DBNAME']
        DBUSER = info['DBUSER']
        DBHOST = info['DBHOST']
        DBPASSWORD = info['DBPASSWORD']
        DBPORT = 5432,
        geoApiKey = info["geoApiKey"]
    
    with open(file ,'r') as f:
        data = f.readlines()

    #parse the data
    ips, rest = [i.split('- -')[0].strip() for i in data],[i.split('- -')[1].strip() for i in data]
    dates, rest2 = [i.split('] ')[0].replace('[','') for i in rest],[i.split('] ')[1] for i in rest]
    dates = [i.replace('/','-').replace(':',' ',1) for i in dates]
    dates = pd.to_datetime(dates).tz_convert('America/Los_Angeles')
    command, rest3 = [i.split(' ',1)[0].replace('"','') for i in rest2],[i.split(' ',1)[1] for i in rest2]
    info, rest4 = [ i.split('" "')[-1] for i in rest3],[ ''.join(i).split('" "')[:-1] for i in rest3]
    altip, rest5 = [''.join(i).split(' "')[-1] for i in rest4],[''.join(i).split(' "')[0] for i in rest4]
    rest6 = [i.split(' ')[-2:] for i in rest5]
    resp, size = [i[0] for i in rest6],[i[1] for i in rest6]
    rest7 = [i.split('" ')[0] if len(i.split('" '))==2 else "None None" for i in rest5]
    resource,proto = [i.split(' ')[0] for i in rest7 ], [i.split(' ')[1] if len(i.split(' '))==2 else 'None' for i in rest7]
    year = [int(i) for i in dates.year]
    month = [int(i) for i in dates.month]
    day = [int(i) for i in dates.day]
    
    print('Done Parsing')
    
    print('Getting GeoData')
    
    #Get geographic origin
    ip_list = list(set(ips))
    ip_ids = {}
    
    for i in range(len(ip_list)):
        if i%50 == 0:
            print('{} Ips of {} ips'.format(i,len(ip_list)))
        urlFoLaction = "http://api.ipstack.com/{}?access_key={}".format(ip_list[i],geoApiKey)
        locationInfo = json.loads(urllib.request.urlopen(urlFoLaction).read())
        ip_ids[ip_list[i]] = locationInfo
    
    #extract fields
    cities = []
    state = []
    country =[]
    lats = []
    lngs = []
    for i in ips:    
        if i in ip_ids.keys():
                if ip_ids[i]['city'] == None:
                    cities.append('El Dorado Lake')
                else:
                    cities.append(ip_ids[i]['city'])
                if ip_ids[i]['region_name'] == None:
                    state.append(ip_ids[i]['country_name'])
                else:
                    state.append(ip_ids[i]['region_name'])
                country.append(ip_ids[i]['country_name'])
                lats.append(ip_ids[i]['latitude'])
                lngs.append(ip_ids[i]['longitude'])
        else:
            cities.append('-')
            state.append('-')
            country.append('-')
            lats.append('-')
            lngs.append('-')   
            
    print('GeoData Processing Done')
    print('Initiated Database table creation')
    


    # Connect to an existing database
    conn = psycopg2.connect(
        dbname=DBNAME,
        user=DBUSER,
        host=DBHOST,
        password=DBPASSWORD,
        port=5432)
# Open a cursor to perform database operations
    cur = conn.cursor()
# Execute a command: this creates a new table
    cur.execute('''DROP TABLE IF EXISTS log_entry;''')
    conn.commit()

    table_name = 'log_entry'

    print('Making TABLE...')
    cur.execute('''
        CREATE TABLE {} (
        id VARCHAR(5000)  PRIMARY KEY,
        ip VARCHAR (5000) NOT NULL,
        date VARCHAR (50) NOT NULL,
        command VARCHAR (5000) NOT NULL,
        resource VARCHAR (5000) NOT NULL,
        proto VARCHAR (5000) NOT NULL,
        response VARCHAR (5000) NOT NULL,
        size VARCHAR (5000) NOT NULL,
        info VARCHAR (5000) NOT NULL,
        lat VARCHAR (5000) NOT NULL,
        lng VARCHAR (5000) NOT NULL,
        city VARCHAR (5000) NOT NULL,
        state VARCHAR (5000) NOT NULL,
        country VARCHAR (5000) NOT NULL,
        year VARCHAR (5000) NOT NULL,
        month VARCHAR (5000) NOT NULL,
        day VARCHAR (5000) NOT NULL);
        '''.format(table_name))
    conn.commit()

    print('TABLE: {} \n Successfully Created'.format(table_name))

    # the correct conversion (no more SQL injections!)
    #cur.execute("INSERT INTO {} (tweet_date, tweet_text, usr_name, hash_tags) VALUES (%s, %s, %s, %s)".format(table_name),
    #        ('-', '-', '-', '-')    
    print('LOADING DATA INTO TABLE: {}'.format(table_name))

    for i in range(len(ips)):

        cur.execute("INSERT INTO log_entry (id, ip, date, command, resource, proto, response, size, info, lat, lng, city, state, country, year, month, day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (i, ips[i], dates[i], command[i], resource[i], proto[i], resp[i], size[i], info[i], lats[i], lngs[i], cities[i], state[i], country[i], year[i], month[i], day[i]))
        conn.commit()

    

    cur.close()
    conn.close()
    
    print("Data has been Processed")
    
    