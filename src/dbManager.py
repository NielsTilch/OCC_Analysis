import csv
import sqlite3
import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from datetime import datetime

csv_path = "external_data/matchs/new_data.csv"




def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """

    db_file = "external_data/database.db"

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn





def select_hour(conn):
    print(0)













def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("""SELECT map.type, COUNT(*) as number_played 
                    FROM MATCH as match, MAP_MAPPING as map
                     WHERE match.map_name = map.map_name
                       GROUP BY map.type
                       ORDER BY number_played """)

    rows = cur.fetchall()

    cars=[]
    data=[]

    for row in rows:
        cars.append(row[0])
        data.append(row[1])
        print(row)

    # Creating explode data
    explode = (0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.0, 0.0)


    # Wedge properties
    wp = {'linewidth': 1, 'edgecolor': "green"}

    # Creating autocpt arguments
    def func(pct, allvalues):
        absolute = int(pct / 100. * np.sum(allvalues))
        return "{:.1f}%\n({:d} g)".format(pct, absolute)

    # Creating plot
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(data,
                                      autopct=lambda pct: func(pct, data),
                                      explode=explode,
                                      labels=cars,
                                      shadow=True,
                                      startangle=90,
                                      wedgeprops=wp,
                                      textprops=dict(color="black"))

    # Adding legend
    ax.legend(wedges, cars,
              title="Map type",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    # show plot
    plt.show()



def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("""SELECT map.type, COUNT(*) as number_played 
                    FROM MATCH as match, MAP_MAPPING as map
                     WHERE match.map_name = map.map_name
                       GROUP BY map.type
                       ORDER BY number_played """)

    rows = cur.fetchall()

    cars=[]
    data=[]

    for row in rows:
        cars.append(row[0])
        data.append(row[1])
        print(row)

    # Creating explode data
    explode = (0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.0, 0.0)


    # Wedge properties
    wp = {'linewidth': 1, 'edgecolor': "green"}

    # Creating autocpt arguments
    def func(pct, allvalues):
        absolute = int(pct / 100. * np.sum(allvalues))
        return "{:.1f}%\n({:d} g)".format(pct, absolute)

    # Creating plot
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(data,
                                      autopct=lambda pct: func(pct, data),
                                      explode=explode,
                                      labels=cars,
                                      shadow=True,
                                      startangle=90,
                                      wedgeprops=wp,
                                      textprops=dict(color="black"))

    # Adding legend
    ax.legend(wedges, cars,
              title="Map type",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    # show plot
    plt.show()


'''
Function of top map (by number of hours played)
'''
def top_map_to_csv(conn,top):
    cur = conn.cursor()
    command = """SELECT map.map_name, COUNT(map.length_hour*60+map.length_minute) as length 
                FROM MATCH as match, MAP_MAPPING as map
                WHERE match.map_name = map.map_name AND map.pool>3
                GROUP BY map.map_name 
                ORDER BY length desc 
                limit """ + str(top)
    cur.execute(command)

    rows = cur.fetchall()

    with open('top_map.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['MAP_NAME', 'TOTAL MINUTES'])
        for row in rows :
            writer.writerow([row[0],row[1]])


"""
Function to create a time series of player activity.
Period : Time spaced between two values (in minutes) 
"""
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

    """
    first_date = {}
    for row in rows:
        print(row)
        first_date['date_day'] = int(row[1])
        first_date['date_month'] = int(row[2])
        first_date['date_year'] = int('20' + str(row[3]))
        first_date['date_hour'] = int(row[4])
        first_date['date_minute'] = int(row[5])
        break

    first_datetime = datetime(year=first_date['date_year'], month=first_date['date_month'], day=first_date['date_day'],
                             hour=first_date['date_hour'], minute=first_date['date_minute'], microsecond=0)

    """
    # Get last recorded match from table
    command_last = """SELECT * 
                        FROM MATCH 
                        ORDER BY ID DESC LIMIT 1"""



    cur.execute(command_last)
    rows = cur.fetchall()
    #Get timestamp of last match (first to be analyzed)
    last_date=rows[0][6]

    """
    for row in rows:
        last_date['date_day']=int(row[1])
        last_date['date_month']=int(row[2])
        last_date['date_year']=int('20'+str(row[3]))
        last_date['date_hour']=int(row[4])
        last_date['date_minute']=int(row[5])
        break

    last_datetime = datetime(year=last_date['date_year'],month=last_date['date_month'],day=last_date['date_day'],
                             hour=last_date['date_hour'],minute=last_date['date_minute'],microsecond=0)

    last_datetime.timestamp()
    """

    first_match_periodPlayerCount=last_date

    #Variable for first activity match
    first_match_saved_activity=0

    #CSV
    csvFilePath='time_series_match-period-'+str(period)+'min.csv'
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

        """
        #Get of first and last interval (day time format)
        datetime_intervalle_first = datetime.fromtimestamp(interval_first)
        datetime_intervalle_last = datetime.fromtimestamp(interval_last)

        dict_intervalle_first={}
        dict_intervalle_last={}

        #Fill Dictionnary First Interval
        dict_intervalle_first['year'] = datetime_intervalle_first.strftime('%Y')
        dict_intervalle_first['month']=datetime_intervalle_first.strftime('%m')
        dict_intervalle_first['day'] = datetime_intervalle_first.strftime('%d')
        dict_intervalle_first['hour'] = datetime_intervalle_first.strftime('%H')
        dict_intervalle_first['minute'] = datetime_intervalle_first.strftime('%M')

        #Fill Dictionnary Last Interval
        dict_intervalle_last['year']=datetime_intervalle_last.strftime('%Y')
        dict_intervalle_last['month'] = datetime_intervalle_last.strftime('%m')
        dict_intervalle_last['day'] = datetime_intervalle_last.strftime('%d')
        dict_intervalle_last['hour'] = datetime_intervalle_last.strftime('%H')
        dict_intervalle_last['minute'] = datetime_intervalle_last.strftime('%M')

        where_query_last='date_year <= '+str(dict_intervalle_last['year'])+' AND date_month <= '+str(dict_intervalle_last['month'])+ ' AND date_day <= ' + str(dict_intervalle_last['day'] + ' AND date_hour <= '+ str(dict_intervalle_last['hour'] + ' AND date_minute <= '+str(dict_intervalle_last['minute'])))
        where_query_first='date_year >= '+str(dict_intervalle_first['year'])+' AND date_month >= '+str(dict_intervalle_first['month'])+ ' AND date_day >= ' + str(dict_intervalle_first['day'] + ' AND date_hour >= '+ str(dict_intervalle_first['hour'] + ' AND date_minute >= '+str(dict_intervalle_first['minute'])))
        """

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



def select_2(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("""SELECT map_name, COUNT(length_hour*60+length_minute) as length
                    FROM MATCH 
                       GROUP BY map_name
                       ORDER BY length desc
                       limit 10""")

    rows = cur.fetchall()

    cars=[]
    data=[]

    for row in rows:
        cars.append(row[0])
        data.append(row[1])
        print(row)

    # Creating explode data


    # Wedge properties
    wp = {'linewidth': 1, 'edgecolor': "green"}

    # Creating autocpt arguments
    def func(pct, allvalues):
        absolute = int(pct / 100. * np.sum(allvalues))
        return "{:.1f}%\n({:d} g)".format(pct, absolute)

    # Creating plot
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(data,
                                      autopct=lambda pct: func(pct, data),
                                      labels=cars,
                                      shadow=True,
                                      startangle=90,
                                      wedgeprops=wp,
                                      textprops=dict(color="black"))

    # Adding legend
    ax.legend(wedges, cars,
              title="Maps",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    # show plot
    plt.show()




def main():
    # create a database connection
    conn = create_connection()
    with conn:
        print("2. Query all tasks")
        #select_all_tasks(conn)
        #select_2(conn)
        #top_map_to_csv(conn=conn,top=50)
        match_time_series(conn,15)
        match_time_series(conn, 5)


if __name__ == '__main__':
    main()