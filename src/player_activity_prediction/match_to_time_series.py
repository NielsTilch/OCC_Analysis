import argparse
import sqlite3
import numpy as np
import pandas as pd
from util.main.database import create_connection

def match_time_series(conn: sqlite3.dbapi2.Connection,period:int) -> None:
    """
    Create the time series csv sheet with a pre-defined period (in minutes)

    :param conn: key connection to database
            period: period between two point of the time series (in minutes)

    :return None
    """



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

        #Exporting dataframe to csv to clear up the cache and RAM for better execution performance
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

        #SQL query line
        query = """ SELECT participants
                    FROM MATCH
                    WHERE """ + str(interval_first) + """ <= date_full AND """ + str(interval_last) + """ >= date_full """

        #Execute SQL query
        cur.execute(query)

        #Retrieve the data
        rows = cur.fetchall()

        #Total activity number of player array
        total_activity = []
        first = True

        #If the number of retrieved rows isn't null, go through the rows
        if len(rows)!=0:

            #For loop to go through the rows
            for row in rows:
                total_activity.append(row[0])

                #Get activity of first match of the batch
                if first:
                    first = False
                    first_match_saved_activity = row[0]

                #Get Mean activity
                mean_activity = np.mean(total_activity)

        #Case if no row returned by the query, we take the closest (by time) number of player recorded
        else:
            mean_activity=first_match_saved_activity


        df2 = pd.DataFrame([[np.ceil(mean_activity)]],
            columns=['activity'])

        #Concatenate the dataframes
        new_df = pd.concat([new_df,df2],axis=0)

    #Add last data to the csv file
    new_df.to_csv(csvFilePath, mode='a', index=False, header=False, sep=";")



parser = argparse.ArgumentParser()
parser.add_argument('--step', type=int, default=15, help='Period step in minutes')
cfg = parser.parse_args()


# create a database connection
conn = create_connection()
with conn:
    match_time_series(conn,cfg.step)