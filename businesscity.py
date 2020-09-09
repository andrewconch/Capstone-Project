import sqlite3
import sys
conn = sqlite3.connect(sys.argv[1])
JavaScriptfile = sys.argv[2]
cur = conn.cursor()

city = input('''Please insert a city where you'd like to gather business information from:''')
state = input('''Please enter the two letter abbreviation for the State, or three letter abbreviation for the province that the city is located in:''')
cur.execute('''
SELECT Business.name, Business.address, Business.latitude, Business.longitude, City.city, State.state
FROM Business
JOIN City JOIN State
ON Business.city_id = City.id AND Business.state_id = State.id
WHERE city =? AND state=?''', (city,state))

fhand = open(JavaScriptfile, 'w')
fhand.write("myData = [\n")
count = 0
citycheck = 0
for row in cur:
    name = row[0]
    address = row[1]
    latitude = row[2]
    longitude = row[3]
    name = name.replace("'", "")
    address = address.replace("'", "")
    citycheck = name
    statecheck = address
    try:
        count = count + 1
        if count > 1: fhand.write(",\n")
        output = "["+str(latitude)+","+str(longitude)+", '"+name+", "+address+"']"
        fhand.write(output)
    except:
            continue

if citycheck == 0:
    print("Either the city or state input were not found in the database, please restart program and try again.")


fhand.write("\n];\n")
cur.close()
fhand.close()
