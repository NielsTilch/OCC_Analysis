import csv
import sqlite3
import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from datetime import datetime

csv_path = "external_data/matchs/data/new_data.csv"




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


if __name__ == '__main__':
    main()