import json
import sqlite3
import sys

conn = sqlite3.connect(sys.argv[1])
jsonFile = sys.argv[2]
#This is the first python script to run in the sequence and allows for quick
#importation of data. Data is filtered and sorted at later steps.
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Business (
id INTEGER PRIMARY KEY UNIQUE,
name TEXT,
address TEXT,
city TEXT,
state TEXT,
zipcode TEXT,
latitude TEXT,
longitude TEXT,
reviews INTEGER,
review_count INTEGER )''')
# generates table in within sqlite file
cur.execute('SELECT COUNT(*) from Business;')
# describes number of entries currently in Database file
count = cur.fetchone()[0]
# number of entries in database

f = open(jsonFile, 'r',encoding="utf8")
# expensive statement, depending on your filesize this might let you run out of memory

print('The current number of entries within the database is:', count)
user_input = input('''
Please select the number of businesses you would like the to extend the database to.
Ensure that the value selected is larger than the current length of the database.
If you select a value larger than the current database count, your previous data
will not be overwritten. This will simply extend the current database to the length
you specify:\n\n''')
try:
    maxbiz = int(user_input)
except ValueError:
    try:
        maxbiz = float(user_input)
        print("Number provided was not a positive integer. Please re-run the program and provide an integer.")
        quit()
    except ValueError:
        print("Input provided was not a positive integer. Please re-run the program and provide an integer.")
        quit()
cur.execute('SELECT max(id) FROM Business')
#will position cursor at max id in current database
#if no ids then will resume at beginnning


try:
    lines = cur.fetchone()
    line = int(lines[0])
except:
    line = -1
if line == -1:

    revu = [json.loads(s) for s in f.readlines()[line+1:maxbiz]]
    for item in revu:
        name = item['name']
        address = item['address']
        city = item['city']
        state = item['state']
        zipcode = item['postal_code']
        latitude = item['latitude']
        longitude = item['longitude']
        reviews = item['stars']
        review_count = item['review_count']
        cur.execute('INSERT OR IGNORE INTO Business (name, address, city, state, zipcode, latitude, longitude, reviews, review_count) VALUES (?,?,?,?,?,?,?,?,?)', (name, address, city, state, zipcode, latitude, longitude, reviews, review_count))
        #will insert items into database if there are no previous entries in database
elif line >= maxbiz:
    print("The number of businesses in the table already exceed the maximum businesses chosen. Please choose a larger maximum number of businesses.")
else:
    revu = [json.loads(s) for s in f.readlines()[line:maxbiz]]
    for item in revu:
        name = item['name']
        address = item['address']
        city = item['city']
        state = item['state']
        zipcode = item['postal_code']
        latitude = item['latitude']
        longitude = item['longitude']
        reviews = item['stars']
        review_count = item['review_count']
        #will append database with entries from current length of database to the input number provided

        cur.execute('INSERT OR IGNORE INTO Business (name, address, city, state, zipcode, latitude, longitude, reviews, review_count) VALUES (?,?,?,?,?,?,?,?,?)', (name, address, city, state, zipcode, latitude, longitude, reviews, review_count))
conn.commit()
f.close()
