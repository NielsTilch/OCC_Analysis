import argparse
import sqlite3
from sqlite3 import Error
import numpy as np
import pandas as pd


def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """

    db_file = "./../external_data/database.db"

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def match_time_series(conn,period):
    period=period*60

    cur = conn.cursor()

    # Get first recorded match from table
    command_first = """SELECT * 
                        FROM MATCH 
                        ORDER BY ID LIMIT 1"""

    cur.execute(command_first)
    rows = cur.fetchall()

    #Get first match (last to be analyzed)
    first_date=rows[0][6]

    # Get last recorded match from table
    command_last = """SELECT * 
                        FROM MATCH 
                        ORDER BY ID DESC LIMIT 1"""



    cur.execute(command_last)
    rows = cur.fetchall()
    #Get timestamp of last match (first to be analyzed)
    last_date=rows[0][6]

    first_match_periodPlayerCount=last_date

    #Variable for first activity match
    first_match_saved_activity=0

    #CSV
    csvFilePath='time_series_match-period-'+str(period)+'s.csv'
    new_df = pd.DataFrame(
        columns=['activity'])

    new_df.to_csv(csvFilePath, index=False, sep=";")

    tracker = 0
    #While loop
    while(first_date<=first_match_periodPlayerCount):
        if tracker%1000==0:
            print("Tracking step number "+str(tracker)+" - "+str(np.floor((first_match_periodPlayerCount-first_date)/(last_date-first_date)*10000)/100)+"% remaining")
            new_df.to_csv(csvFilePath, mode='a', index=False, header=False, sep=";")
            new_df = pd.DataFrame(
                columns=['activity'])

        tracker += 1

        #Tracking of step
        first_match_periodPlayerCount = first_match_periodPlayerCount-period

        #Get first and last interval (timestamp format)
        interval_first = first_match_periodPlayerCount
        interval_last = first_match_periodPlayerCount + period

        query = """ SELECT participants
                    FROM MATCH
                    WHERE """ + str(interval_first) + """ <= date_full AND """ + str(interval_last) + """ >= date_full """

        cur.execute(query)
        rows = cur.fetchall()

        total_activity = []
        first = True
        if len(rows)!=0:
            for row in rows:
                total_activity.append(row[0])

                #Get activity of first match of the batch
                if first:
                    first = False
                    first_match_saved_activity = row[0]

                #Get Mean activity
                mean_activity = np.mean(total_activity)
        else:
            mean_activity=first_match_saved_activity


        df2 = pd.DataFrame([[np.ceil(mean_activity)]],
            columns=['activity'])

        new_df = pd.concat([new_df,df2],axis=0)


    new_df.to_csv(csvFilePath, mode='a', index=False, header=False, sep=";")



parser = argparse.ArgumentParser()
parser.add_argument('--step', type=int, default=15, help='Period step in minutes')
cfg = parser.parse_args()


# create a database connection
conn = create_connection()
with conn:
    match_time_series(conn,cfg.step)