import argparse
from sqlite3 import Error
import util.main.database as db
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, default="new_data.csv", help='Path of the file name')
cfg = parser.parse_args()

#Database connection
conn = db.create_connection()

#Reset match table
db.reset_match_table(conn=conn)

#Read the dataset
df = pd.read_csv('data/new_data.csv', sep=";")

#Go through all of the matchs to query to the database
for i, row in df.iterrows():

    #Counter
    if i % 1000 == 0:
        print('Item number ', i, ' done ...')
        conn.commit()

    # Avoiding duplication error due to unique key
    try:
        print(type(row))
        #Query
        db.insert_match(conn=conn,values=row,id=i)

    #Print Errors
    except Error as e:
        print(e)
        print('Match : ',row['map_name'], ' line number : ',i)

conn.commit()