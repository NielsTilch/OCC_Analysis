import csv
import sqlite3
from sqlite3 import Error, Connection
from numpy import array
from pandas import DataFrame

db_file_path = "external_data/database.db"


def create_connection() -> Connection | None:
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """

    try:
        conn = sqlite3.connect(db_file_path)
        return conn
    except Error as e:
        print(e)
        raise Exception('Could not connect to database !')


def test_map_exists(conn: sqlite3.dbapi2.Connection, map_name: str) -> bool:
    """
    Test if the map (name_map) exist in database

    :param conn: Database connection
    :param map_name: Name of the map
    :return: If map exists (True) or not (False)
    """
    cur = conn.cursor()
    command = """
                SELECT 
                    map_name, COUNT(length_hour*60+length_minute) as length 
                    
                FROM 
                    MAP_MAPPING
                    
                WHERE 
                    map_name = '""" + str(map_name) + """'
            """
    cur.execute(command)
    rows = cur.fetchall()
    conn.commit()

    if not len(rows):
        return False
    return True


def add_specific_attribute_to_map(conn: sqlite3.dbapi2.Connection, map_name: str, attribute: str, value: int) -> None:
    """
    Add a specific argument to a map in database

    :param conn: Database connection
    :param map_name: Name of the map
    :param argument: Name of the argument
    :param value: Value of the argument
    :return: None
    """

    if test_map_exists(conn=conn, map_name=map_name):
        command = """
                    UPDATE 
                        MAP_MAPPING 
                        
                    SET 
                        """ + attribute + """ = """ + str(value) + """
                        
                    WHERE
                        MAP_NAME='""" + map_name + """'"""
        cur = conn.cursor()
        cur.execute(command)
        conn.commit()
    else:
        raise Exception("Map " + map_name + " doesn't exist in database !")


def add_attributes_to_map(conn: sqlite3.dbapi2.Connection, map_name: str, values: array) -> None:
    """
    Add an array of value for map's attributes

    :param conn: Connection to the database
    :param map_name: Name of the map
    :param values: Array of the values of the attributes
    :return: None
    """

    command = """
                UPDATE 
                    MAP_MAPPING 

                SET 
                    distance_spawns=""" + str(values[4]) + """,
                    time_to_objective=""" + str(values[5]) + """,
                    time_to_interception=""" + str(values[6]) + """,
                    time_to_own_objective=""" + str(values[7]) + """,
                    width_main_lane=""" + str(values[8]) + """,
                    width_objective_lane=""" + str(values[9]) + """,
                    water_link_ratio=""" + str(values[10]) + """,
                    level_armor=""" + str(values[11]) + """,
                    level_gear=""" + str(values[12]) + """, 
                    defense_gear_level=""" + str(values[13]) + """, 
                    time_tunneling_to_wool_grab=""" + str(values[14]) + """,
                    mean_time_to_first_capture=""" + str(values[15]) + """,
                    slowness_when_capture_level=""" + str(values[16]) + """,
                    number_of_path_to_objective=""" + str(values[17]) + """

                WHERE
                    MAP_NAME='""" + map_name + """'
            """

    cur = conn.cursor()

    try:
        cur.execute(command)
        conn.commit()
    except Error as e:
        raise e


def top_map_to_df(conn: sqlite3.dbapi2.Connection, top: int) -> DataFrame:
    """
    Return the top n map played

    :param conn: Connection to the database
    :param top: Integer as the number of map return
    :return: Dataframe of the maps and the total of minutes played ['Map name, 'Minutes played', 'Path file', 'Coords']
    """

    command = """
                SELECT 
                    map.map_name, COUNT(match.length_hour*60+match.length_minute) as length, map.PATH, map.COORDS
                    
                FROM 
                    MAP_MAPPING as map, MATCH as match

                WHERE 
                    map.map_name=match.map_name
                    
                GROUP BY 
                    map.map_name 
                    
                ORDER BY 
                    length desc 
                    
                limit """ + str(top)

    cur = conn.cursor()
    cur.execute(command)

    rows = cur.fetchall()

    return DataFrame(rows, columns=['Map name', 'Minutes played','Path file', 'Coords'])


def specific_top_map_to_df(conn: sqlite3.dbapi2.Connection, top: int,mode: str) -> DataFrame:
    """
    Return the top n map played with the specific mode marker

    :param conn: Connection to the database
    :param top: Integer as the number of map return
    :return: Dataframe of the maps and the total of minutes played ['Map name, 'Minutes played', 'Path file', 'Coords']
    """

    #Checks
    if mode=="":
        raise Exception('Mode parameter is null !')

    if top < 1:
        raise Exception('Top parameter must be strictly positive !')

    command = """
                SELECT 
                    map.map_name, COUNT(match.length_hour*60+match.length_minute) as length, map.PATH, map.COORDS

                FROM 
                    MAP_MAPPING as map, MATCH as match

                WHERE 
                    map.map_name=match.map_name AND map.GAMEMODE = '"""+mode+"""'

                GROUP BY 
                    map.map_name 

                ORDER BY 
                    length desc 

                limit """ + str(top)

    cur = conn.cursor()
    cur.execute(command)

    rows = cur.fetchall()

    return DataFrame(rows, columns=['Map name', 'Minutes played','Path file', 'Coords'])







def get_specific_map(conn: sqlite3.dbapi2.Connection, map_name: str) -> list:
    """
    Get the database output of a specific map

    :param conn: Connection to the database
    :param map_name: Name of the map
    :return: The row of the map in the database
    """

    cur = conn.cursor()
    command_first = """
                        SELECT 
                            * 
                            
                        FROM 
                            MAP_MAPPING 
                                    
                        WHERE 
                            MAP_NAME = '""" + str(map_name) + """'"""

    cur.execute(command_first)
    return cur.fetchall()


def reset_match_table(conn: sqlite3.dbapi2.Connection) -> None:
    """
    Reset 'MATCH' table

    :param conn: Connection to the database
    :return:
    """

    drop_map_mapping = "DROP TABLE `MATCH`;"
    create_map_mapping = """CREATE TABLE `MATCH` (
    	`ID` INT NOT NULL,
    	`date_day` INT NOT NULL,
    	`date_month` INT NOT NULL,
    	`date_year` INT NOT NULL,
    	`date_hour` INT NOT NULL,
    	`date_minute` INT NOT NULL,
    	`date_full` BIGINT(20) NOT NULL,
    	`map_name` VARCHAR NOT NULL,
    	`length_hour` INT NOT NULL,
    	`length_minute` INT NOT NULL,
    	`length_second` INT NOT NULL,
    	`participants` INT NOT NULL,
    	`winner` VARCHAR,
    	`cloudy_ver` INT NOT NULL,
    	PRIMARY KEY (`ID`)
    );"""

    cur = conn.cursor()
    try:
        cur.execute(drop_map_mapping)
    except:
        print("Table MATCH doesn't exist")
    cur.execute(create_map_mapping)
    conn.commit()
    cur.close()


def insert_match(conn: sqlite3.dbapi2.Connection, values, id: int) -> None:
    cur = conn.cursor()

    # Query
    insert_map_query = """INSERT INTO MATCH 
            (ID,date_day,date_month,date_year,date_hour,date_minute,date_full,map_name,length_hour,length_minute,length_second,participants,winner,cloudy_ver) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

    # Variables of the query
    data = (
        id,
        values['date_day'],
        values['date_months'],
        values['date_year'],
        values['date_hour'],
        values['date_minute'],
        values['date_full'],
        values['map_name'],
        values['length_hour'],
        values['length_minute'],
        values['length_second'],
        values['participants'],
        values['winner'],
        values['cloudy_ver']
    )

    cur.execute(insert_map_query, data)


def reset_map_table(conn: sqlite3.dbapi2.Connection) -> None:
    drop_map_mapping = "DROP TABLE `MAP_MAPPING`;"
    create_map_mapping = """CREATE TABLE `MAP_MAPPING` (
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
    	`time_tunneling_to_objective` INT,
    	`mean_time_to_first_capture` INT,
    	`slowness_when_capture_level` INT,
    	`number_of_path_to_objective` INT,
    	`PATH` VARCHAR NOT NULL,
    	`COORDS` VARCHAR NOT NULL,
    	PRIMARY KEY (`MAP_NAME`)
    );"""
    cur = conn.cursor()

    cur.execute(drop_map_mapping)
    conn.commit()

    cur.execute(create_map_mapping)
    conn.commit()

    cur.close()


def insert_map(conn: sqlite3.dbapi2.Connection, map_name: str, mode_type: str, pool: str, authors_string: str, path: str, coords: str) -> None:
    cur = conn.cursor()

    try:
        insert_map_query = "INSERT INTO MAP_MAPPING (MAP_NAME,GAMEMODE, POOL, AUTHORS, PATH, COORDS) VALUES (?,?,?,?,?,?) "
        map_data = (map_name, mode_type, pool, authors_string, path, coords)
        cur.execute(insert_map_query, map_data)
        conn.commit()

        # Avoiding duplication error due to unique key
    except Error as e:
        print('Duplicate avoided')
        print(e)

    cur.close()


top_map_to_df(conn=create_connection(), top=15)
