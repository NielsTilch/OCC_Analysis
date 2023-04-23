import sqlite3
from sqlite3 import Error

database = "./database.db"

#Database connection
conn = None
try:
    conn = sqlite3.connect(database=database)
except Error as e:
    print(e)

cur = conn.cursor()

#For loop until break
while(True):

    #Input map
    input_map = str(input("Name of the map (blank if you want to stop)"))

    if input_map != "":
        #Command (I know you can sql inject)
        command_first = """SELECT * 
                                FROM MATCH 
                                WHERE MAP_NAME = """+str(input_map)

        cur.execute(command_first)

        rows = cur.fetchall()
        if len(rows)>0:
            print("rest")
            #Input of all of the possible added attributes
            #blank input if NULL
            #Insert INTO table
        else:
            print("Map "+str(input_map)+"doesn't exist")
    else:
        break;