
"""
     Contains database configurations
"""
import os
import sys
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash
from instance.config import config


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
    
    create_user_table_query= """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            fullname VARCHAR (124) NOT NULL,
            username VARCHAR (124) NOT NULL UNIQUE,           
            email VARCHAR (255) NOT NULL,
            password VARCHAR (255) NOT NULL
        )
        """
    create_group_table_query="""
        CREATE TABLE IF NOT EXISTS groups(
            group_id SERIAL PRIMARY KEY,
            creator_id INTEGER,
            FOREIGN KEY(creator_id) REFERENCES users(Id),
            group_title VARCHAR(128) NOT NULL,
            group_description VARCHAR(255), 
            created_on TIMESTAMP NOT NULL DEFAULT now()

        )
        """

    create_members_table_query="""
        CREATE TABLE IF NOT EXISTS members(
             member_id SERIAL PRIMARY KEY,
             email VARCHAR(124) NOT NULL,
             groupId INTEGER,
             group_name VARCHAR(124),
             FOREIGN KEY(groupId) REFERENCES groups(group_id),
             time_added TIMESTAMP DEFAULT now()
        )    
        """
    return [create_user_table_query, create_group_table_query, create_members_table_query]

def drop_table_if_exists():
    drop_table_users= """DROP TABLE IF EXISTS users"""
    return [drop_table_users]


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


def add_data_to_db(query):
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