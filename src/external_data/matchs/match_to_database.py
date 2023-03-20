import argparse
import sqlite3
from sqlite3 import Error

import pandas as pd

database = "./../database.db"


parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, default="new_data.csv", help='Path of the file name')
cfg = parser.parse_args()


#Database connection
conn = None
try:
    conn = sqlite3.connect(database=database)
except Error as e:
    print(e)

#Commend to create table mapping
drop_map_mapping="DROP TABLE `MATCH`;"
create_map_mapping="""CREATE TABLE `MATCH` (
	`ID` INT NOT NULL,
	`date_day` INT NOT NULL,
	`date_month` INT NOT NULL,
	`date_year` INT NOT NULL,
	`date_hour` INT NOT NULL,
	`date_minute` INT NOT NULL,
	`date_full` BIGINT(20) NOT NULL,
	`map_name` VARCHAR NOT NULL,
	`length_hour` INT NOT NULL,
	`length_minute` INT NOT NULL,
	`length_second` INT NOT NULL,
	`participants` INT NOT NULL,
	`winner` VARCHAR,
	`cloudy_ver` INT NOT NULL,
	PRIMARY KEY (`ID`)
);"""

cur = conn.cursor()
try:
    cur.execute(drop_map_mapping)
except:
    print("Table MATCH already created")
cur.execute(create_map_mapping)


#Read the dataset
df = pd.read_csv('new_data.csv',sep=";")

#Go through all of the matchs to query to the database
for i, row in df.iterrows():

    #Counter
    if i % 1000 == 0:
        print('Item number ', i, ' done ...')
        conn.commit()

    # Avoiding duplication error due to unique key
    try:

        #Query
        insert_map_query = """INSERT INTO MATCH 
        (ID,date_day,date_month,date_year,date_hour,date_minute,date_full,map_name,length_hour,length_minute,length_second,participants,winner,cloudy_ver) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

        #Variables of the query
        data = (i,row['date_day'], row['date_months'], row['date_year'], row['date_hour'], row['date_minute'],row['date_full'] ,row['map_name'], row['length_hour'],
                 row['length_minute'], row['length_second'], row['participants'], row['winner'], row['cloudy_ver'])

        cur.execute(insert_map_query, data)


    #Print Errors
    except Error as e:
        print(e)
        print('Match : ',row['map_name'], ' line number : ',i)

conn.commit()