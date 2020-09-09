# ProgrammingProjects

Please excuse my GitHub page if it is confusing, this is my first time using GitHub to post my own work! 

Just a brief collection of my programming work from various courses that I have done.

The work has been separated into two different directories. In the main directory you will find files contaning my work from the Python for Everybody Capstone project. The genomicdatascience directory contains some of my work from the Johns Hopkins Genomic Data Science specialization.

The capstone project for the Python for Everybody specialization was a small project that incorporated Python, a bit of SQL and very limited JavaScript and HTML. The project imports information from a Yelp dataset that is presented in JSON format (business.json). The information is written to a database using the SQLite3 module available for Python by executing rawdatabaseinput.py. Once information is stored in the database, the database is refined by executing jsonbusinessclean.py.

jsonbusinessclean.py established distinct tables for the values City, State and Zipcode. These tables contain the primary key associated with each city, state or zipcode. Replacing the values within the Business table with the foreign key referring to city, state or zipcode allows for a small reduction in file size and easier parsing through database entries.

After creating a refined database, use businesscity.py to select a city and its corresponding state that you are interested in. businesscity.py will export all database entries that contain both the city and state that you specified into a JavaScript file that is parsable by the Google Maps API.

The final step is to execute business.html file which will open a map containing waypoints the business located in the specified city and state. Hovering over the waypoints will provide you with the business name, as well as the address listed for the business.

Here is an example workflow of the Capstone Project:

python rawdatabaseinput.py [json input file] [raw_database.sqlite]

python jsonbusinessclean.py [raw_database.sqlite] [refined_database.sqlite]

python businesscity.py [refined_database.sqlite] [JavaScriptFileOutput]

start chrome business.html
