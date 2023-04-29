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
        return None


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
                    map.map_name, COUNT(map.length_hour*60+map.length_minute) as length 
                    
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


def top_map_to_df(conn: sqlite3.dbapi2.Connection,top: int):
    """
    Return the top n map played

    :param conn: Connection to the database
    :param top: Integer as the number of map return
    :return: Dataframe of the maps and the total of minutes played ['Map name, 'Minutes played']
    """

    command = """
                SELECT 
                    map_name, COUNT(length_hour*60+length_minute) as length 
                    
                FROM 
                    MATCH
                    
                WHERE 
                    map_name = map_name
                    
                GROUP BY 
                    map_name 
                    
                ORDER BY 
                    length desc 
                    
                limit """ + str(top)

    cur = conn.cursor()
    cur.execute(command)

    rows = cur.fetchall()

    return DataFrame(rows, columns=['Map name','Minutes played'])


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

top_map_to_df(conn=create_connection(),top=15)