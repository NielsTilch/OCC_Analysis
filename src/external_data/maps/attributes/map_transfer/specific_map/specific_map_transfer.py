import util.main.database as db

map_name = str(input('Map name : '))

if map_name=="":
    raise Exception('Map name input empty !')

# Connection to database
conn = db.create_connection()
df_path = db.get_specific_map(conn=conn,map_name=map_name)

if not (len(df_path)):
    raise Exception("Map doesn't exist")

file =open('external_data/maps/attributes/map_transfer/file.txt','w')
for element in df_path.iterrows():
    #Writing path of map in folder
    file.write(element[1][2][1:]+'\n')
    #Writing
    file.write('For '+str(element[1][0])+' : /tp '+str(element[1][3])+'\n')
file.close()