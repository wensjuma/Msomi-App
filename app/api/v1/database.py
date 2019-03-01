
"""
     Contains database configurations
"""
import os
import sys
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash
from config import app_config


#db_url= "dbname='politico' host='127.0.0.1' port='5432' user='postgres' password='root'",
def db_init(DB_URL=None):
    
    try:
        conn, cursor = connect_db()
        create_db_query = drop_table_if_exists() + create_tables()
        i = 0
        while i != len(create_db_query):
            query = create_db_query[i]
            cursor.execute(query)
            conn.commit()
            i += 1
        print("--"*50)
        conn.close()

    except Exception as error:
        print("\nProblem Executing Query : {} \n".format(error))


def create_tables():
    #CREATES TABLE FOR users IF THEY DONT EXIST
    
    create_user_query= """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username VARCHAR (124) NOT NULL UNIQUE,
            firstname VARCHAR (124) NOT NULL,
            lastname VARCHAR (124) NOT NULL,
            email VARCHAR (255) NOT NULL,
            password VARCHAR (255) NOT NULL
        )
        """
    return [create_user_query]

def drop_table_if_exists():
    return


def connect_db(query=None, DB_URL=None):
    """
        Connection to the database
    """
    conn = None
    cursor = None
    if DB_URL is None:
        DB_URL = os.getenv('DATABASE_URL') 
        print(DB_URL)

    try:
        # connect to db
        conn = psycopg2.connect(DB_URL)
        print("\n\nConnected {}\n".format(conn.get_dsn_parameters()))
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if query:
            
            cursor.execute(query)
            conn.commit()

    except(Exception,
           psycopg2.DatabaseError,
           psycopg2.ProgrammingError) as error:
        print("DB ERROR: {}".format(error))

    return conn, cursor


def query_data_from_db(query):
    """
        Handles INSERT queries
    """
    try:
        conn = connect_db(query)[0]
        conn.close()
    except psycopg2.Error as _error:
        sys.exit(1)


def select_data_from_db(query):
    """
        Handles SELECT queries
    """
    rows = None
    conn, cursor = connect_db(query)
    if conn:
        
        rows = cursor.fetchall()
        conn.close()

    return rows


if __name__ == '__main__':
    db_init()
    connect_db()