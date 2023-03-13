import sqlite3
import sqlite3
from sqlite3 import Error

csv_path = "external_data/matchs/new_data.csv"




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


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()

    for row in rows:
        print(row)



def main():


    # create a database connection
    conn = create_connection()



    with conn:

        print("2. Query all tasks")
        select_all_tasks(conn)


if __name__ == '__main__':
    main()