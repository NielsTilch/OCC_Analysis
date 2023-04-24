import sqlite3
from sqlite3 import Error

import requests

database = "./../database.db"

#Database connection
conn = None
try:
    conn = sqlite3.connect(database=database)
except Error as e:
    print(e)
    exit(1)

#Commend to create table mapping
drop_map_mapping="DROP TABLE `MAP_MAPPING`;"
create_map_mapping="""CREATE TABLE `MAP_MAPPING` (
	`MAP_NAME` VARCHAR NOT NULL,
	`GAMEMODE` VARCHAR NOT NULL,
	`POOL` VARCHAR NOT NULL,
	AUTHORS VARCHAR,
	`distance_spawns` INT,
	`time_to_objective` INT,
	`time_to_interception` INT,
	`time_to_own_objective` INT,
	`width_main_lane` INT,
	`width_objective_lane` INT,
	`water_link_ratio` INT,
	`level_armor` INT,
	`level_gear` INT,
	`defense_gear_level` INT,
	`time_tunneling_to_wool_grab` INT,
	`mean_time_to_first_capture` INT,
	`slowness_when_capture_level` INT,
	`number_of_path_to_objective` INT,
	PRIMARY KEY (`MAP_NAME`)
);"""

cur = conn.cursor()
cur.execute(drop_map_mapping)
cur.execute(create_map_mapping)

conn.commit()


f = open("list_path_xmls.txt", "r")
lines = f.readlines()

tracker=0

#Go through all of the maps
for path in lines:
    tracker += 1
    if tracker % 10 == 0:
        print('Map number ', tracker, ' done ...')


    mode_type = str(path.split('/')[2])
    map_name=""
    player_max = -1
    authors=[]
    f_map=None
    try:
        f_map = open(path[:-1],"r",encoding="utf8")
    except:
        print('File not recognize : ',path)


    if f_map is not None:
        content_xml = f_map.readlines()
        for xml_lines in content_xml:

            #Detection map name
            if len(xml_lines.split('<name>'))==2:
                map_name = str(xml_lines.split('>')[1].split('<')[0])


                #Number player max
            if len(xml_lines.split('<players max="'))==2:
                try:
                    player_max = int((xml_lines.split('<players max="'))[1].split('"')[0])
                except :
                    print("Problem with player max detection")
                    print("Map : ",map_name)
                    print("String : ",xml_lines.split('<players max="'))



            #Authors
            if len(xml_lines.split('<author uuid="')) == 2:
                try:
                    authors.append((xml_lines.split('<author uuid="'))[1].split('"')[0])
                except:
                    print("Problem with author split")
                    print("Map : ",map_name)
                    print("String : ",xml_lines.split('<author uuid="'))

    authors_string=""
    for i,uuid in enumerate(authors):
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()
        if i==0:
            authors_string = data["name"]
        else :
            authors_string = authors_string + "," + data["name"]

    #Pool naming
    pool=""
    if (player_max ==-1):
        pool="other"
    elif (player_max<5):
        pool="pico"
    elif (player_max<15):
        pool='nano'
    elif (player_max<25):
        pool='micro'
    elif (player_max < 40):
        pool="milli"
    elif (player_max < 58):
        pool = "centi"
    elif (player_max < 72):
        pool = "hecto"
    elif (player_max < 90):
        pool = "mega"
    else :
        pool = "giga"

    #Avoiding duplication error due to unique key
    try:
        insert_map_query = "INSERT INTO MAP_MAPPING (MAP_NAME,GAMEMODE, POOL, AUTHORS) VALUES (?,?,?,?) "
        map_data=(map_name,mode_type,pool,authors_string)
        cur.execute(insert_map_query,map_data)

        conn.commit()
    except Error as e:
        print('Duplicate avoided')
        print(e)

cur.close()
conn.close()