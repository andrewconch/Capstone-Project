import sqlite3
import sys
#pass in raw database file, followed by desired filename of refined database
conn = sqlite3.connect(sys.argv[2])
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Business''')
cur.execute('''DROP TABLE IF EXISTS City''')
cur.execute('''DROP TABLE IF EXISTS State''')
cur.execute('''DROP TABLE IF EXISTS Zipcode''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Business ( id INTEGER PRIMARY KEY UNIQUE, name TEXT, address, city_id INTEGER, state_id INTEGER, zipcode_id INTEGER, reviews INTEGER, review_count INTEGER, latitude FLOAT, longitude FLOAT )''')
cur.execute('''
CREATE TABLE IF NOT EXISTS City ( id INTEGER PRIMARY KEY UNIQUE, city TEXT UNIQUE)''')
cur.execute('''
CREATE TABLE IF NOT EXISTS State ( id INTEGER PRIMARY KEY UNIQUE, state TEXT UNIQUE)''')
cur.execute('''
CREATE TABLE IF NOT EXISTS Zipcode ( id INTEGER PRIMARY KEY UNIQUE, zipcode TEXT UNIQUE)''')


conn_1 = sqlite3.connect(sys.argv[1])
cur_1 = conn_1.cursor()

cities = dict()
states = dict()
zipcodes = dict()
cur_1.execute('''SELECT name, address, city, state, zipcode, reviews, review_count, latitude, longitude FROM Business''')
allbusinesses = list()
for message_row in cur_1:
    name = message_row[0]
    address = message_row[1]
    city = message_row[2]
    state = message_row[3]
    zipcode = message_row[4]
    reviews = message_row[5]
    review_count = message_row[6]
    latitude = message_row[7]
    longitude = message_row[8]

    city_id = cities.get(city,None)
    state_id = states.get(state,None)
    zipcode_id = zipcodes.get(zipcode,None)

    #generates empty dictionaries. Cities, states or zipcode IDs will be saved in a dictionary
    #key value pairs are represented by state/city/zipcode: ID in relational table.
    #We are able to reduce dictionary size by performing this, allows for replacement of
    #redundant text with integers

    allbusinesses.append(message_row[0])
    if city_id is None:
        cur.execute('INSERT OR IGNORE INTO City (city) VALUES (?)', (city,))
        conn.commit()
        cur.execute('SELECT id FROM City WHERE city=?', (city,))
        try:
            row = cur.fetchone()
            city_id = row[0]
            cities[city] = city_id
            #if the city does not exist in dictionary, this will add the city as a key
            #and the corresponding id in the relational table as a value.
        except:
            break
    if state_id is None:
        cur.execute('INSERT OR IGNORE INTO State (state) VALUES (?)', (state,))
        conn.commit()
        cur.execute('SELECT id FROM State WHERE state=?', (state,))
        try:
            row = cur.fetchone()
            state_id = row[0]
            states[state] = state_id
            #if the state does not exist in dictionary, this will add the state as a key
            #and the corresponding id in the relational table as a value.
        except:
            break
    if zipcode_id is None:
        cur.execute('INSERT OR IGNORE INTO Zipcode (zipcode) VALUES (?)', (zipcode,))
        conn.commit()
        cur.execute('SELECT id FROM Zipcode WHERE zipcode=?', (zipcode,))
        try:
            row = cur.fetchone()
            zipcode_id = row[0]
            zipcodes[zipcode] = zipcode_id
            #if the zipcode does not exist in dictionary, this will add the zipcode as a key
            #and the corresponding id in the relational table as a value.
        except:
            break
    cur.execute('INSERT OR IGNORE INTO Business (name, address, city_id, state_id, zipcode_id, reviews, review_count, latitude, longitude) VALUES (?,?,?,?,?,?,?,?,?)', (name, address, city_id, state_id, zipcode_id, reviews, review_count,latitude,longitude))
print("Loaded all businesses, quantity:", len(allbusinesses))

#error with code where a portion of businesses do not get addeded to the refined database.
#unsure of cause of the issue. Attempted to troubleshoot by targeting database entries in
#the business.sqlite file that did not havea city/zipcode/state. Still unsure of the
#underlying issue.
