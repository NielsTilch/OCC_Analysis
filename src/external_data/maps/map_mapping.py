import util.main.database as db
import requests


#Database connection
conn = db.create_connection()

#Commend to create table mapping
db.reset_map_table(conn=conn)

f = open("external_data/maps/list_path_xmls.txt", "r")
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

    db.insert_map(conn=conn,map_name=map_name,mode_type=mode_type,pool=pool,authors_string=authors_string)

conn.close()