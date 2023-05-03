import util.main.database as db

top = int(input('Number of map for the transfer : '))
mode = str(input("Specific gamemode filter (keep blank if you don't want it) : "))

# Connection to database
conn = db.create_connection()

if mode == "":
    df_path = db.top_map_to_df(conn=conn, top=top)
else:
    df_path = db.specific_top_map_to_df(conn=conn, top=top, mode=mode)

if not (len(df_path)):
    raise Exception('Query empty (probably due to input gamemode inexistency) !')

file =open('external_data/maps/attributes/map_transfer/file.txt','w')
for element in df_path.iterrows():

    #Writing path of map in folder
    file.write(element[1][2][1:]+'\n')

    #Writing
    file.write('For '+str(element[1][0])+' : /tp '+str(element[1][3])+'\n')
file.close()