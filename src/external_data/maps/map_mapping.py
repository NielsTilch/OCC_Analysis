import sqlite3
from sqlite3 import Error

database = "./../database.db"

#Database connection
conn = None
try:
    conn = sqlite3.connect(database=database)
except Error as e:
    print(e)

#Commend to create table mapping
drop_map_mapping="DROP TABLE `MAP_MAPPING`;"
create_map_mapping="""CREATE TABLE `MAP_MAPPING` (
	`MAP_NAME` VARCHAR,
	`TYPE` VARCHAR,
	PRIMARY KEY (`MAP_NAME`)
);"""

cur = conn.cursor()
cur.execute(drop_map_mapping)
cur.execute(create_map_mapping)

f = open("list_path_xmls.txt", "r")
lines = f.readlines()

i=0
for path in lines:
    i+=1
    if i % 100 == 0:
        print('Map number ', i, ' done ...')

    mode_type = str(path.split('/')[2])
    map_name=""
    f_map=None
    try:
        f_map = open(path[:-1],"r",encoding="utf8")
    except:
        print('File not recognize : ',path)


    if f_map is not None:
        content_xml = f_map.readlines()
        for xml_lines in content_xml:
            if len(xml_lines.split('<name>'))==2:
                map_name = str(xml_lines.split('>')[1].split('<')[0])

    #Avoiding duplication error due to unique key
    try:
        insert_map_query = "INSERT INTO MAP_MAPPING (MAP_NAME,TYPE) VALUES (?,?) "
        map_data=(map_name,mode_type)
        cur.execute(insert_map_query,map_data)

        conn.commit()
    except:
        print('Duplicate avoided')