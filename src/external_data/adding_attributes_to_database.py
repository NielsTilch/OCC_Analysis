import sqlite3
from sqlite3 import Error
import numpy as np

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
                                FROM MAP_MAPPING 
                                WHERE MAP_NAME = '"""+str(input_map)+"""'"""

        cur.execute(command_first)

        test_rows = cur.fetchall()
        if len(test_rows)>0:
            rows=[]
            rows = np.array(test_rows[0])

            print("Put nothing if nothing is needed to change")
            #Input of all of the possible added attributes

            #Attribute distance_spawns
            input_distance_spawns = int(input("Distance between spawns (in blocks) : "))
            if input_distance_spawns!="":
                rows[4]=input_distance_spawns

            #Attribute time_to_objective
            input_time_to_objective =int(input("Time to objective (in seconds) : "))
            if input_time_to_objective !="":
                rows[5]=input_time_to_objective

            #Attribute time_to_interception
            input_time_to_interception = int(input("Time to interception (in seconds) : "))
            if input_time_to_interception !="":
                rows[6]=input_time_to_interception

            #Attribute time_to_own_objective
            input_time_to_own_objective = int(input("Time to own objective (in seconds) : "))
            if input_time_to_own_objective != "":
                rows[7]=input_time_to_own_objective

            #Attribute width_main_lane
            input_width_main_lane = int(input("Width of main lane (in blocks) : "))
            if input_width_main_lane != "":
                rows[8]=input_width_main_lane

            #Attribute width_objective_lane
            input_width_objective_lane = int(input("Width of objective lane (in blocks) : "))
            if input_width_objective_lane != "":
                rows[9]=input_width_objective_lane

            #Attribute water_lane_ratio
            input_water_lane_ration = int(input("Water lane ratio ( 'water lane size' / 'distance spawn to objective' ) (in blocks) : "))
            if input_water_lane_ration != "":
               rows[10]=input_water_lane_ration

            #Attribute level_armor
            input_level_armor = int(input("Level of armor : "))
            if input_level_armor != "":
                rows[11]=input_level_armor

            #Attribute level_gear
            input_level_gear = int(input("Level of gear"))
            if input_level_gear != "":
               rows[12]=input_level_gear

            #Attribute defense_gear_level
            input_defense_gear_level = int(input("Defense gear level : "))
            if input_defense_gear_level != "":
               rows[13]=input_defense_gear_level

            #Attribute time_tunneling_to_objective
            input_time_tunneling_to_objective = int(input("Time tunneling to objective (in seconds) : "))
            if input_time_tunneling_to_objective != "":
                rows[14]=input_time_tunneling_to_objective

            #Attribute mean_time_to_first_capture
            input_mean_time_to_first_capture = int(input("Mean time to first capture : "))
            if input_mean_time_to_first_capture != "":
                rows[15]=input_mean_time_to_first_capture

            #Attribute slowness_when_capture_level
            input_slowness_when_capture_level=int(input("Slowness level when capture : "))
            if input_slowness_when_capture_level !="":
                rows[16]=input_slowness_when_capture_level

            #Attribute number_of_path_to_objective
            input_number_of_path_to_objective=int(input("Number of path to objective : "))
            if input_number_of_path_to_objective !="":
                rows[17]=input_number_of_path_to_objective

            a = 0
            insert_map_query = """
                                UPDATE 
                                        MAP_MAPPING 
                                    
                                SET 
                                    distance_spawns="""+str(rows[4])+""",
                                    time_to_objective="""+str(rows[5])+""",
                                    time_to_interception="""+str(rows[6])+""",
                                    time_to_own_objective="""+str(rows[7])+""",
                                    width_main_lane="""+str(rows[8])+""",
                                    width_objective_lane="""+str(rows[9])+""",
                                    water_link_ratio="""+str(rows[10])+""",
                                    level_armor="""+str(rows[11])+""",
                                    level_gear="""+str(rows[12])+""", 
                                    defense_gear_level="""+str(rows[13])+""", 
                                    time_tunneling_to_wool_grab="""+str(rows[14])+""",
                                    mean_time_to_first_capture="""+str(rows[15])+""",
                                    slowness_when_capture_level="""+str(rows[16])+""",
                                    number_of_path_to_objective="""+str(rows[17])+"""
                                
                                WHERE
                                    MAP_NAME='"""+str(rows[0])+"""'"""
            print(insert_map_query)
            cur.execute(insert_map_query)
            conn.commit()

        else:
            print("Map "+str(input_map)+"doesn't exist")
    else:
        break;