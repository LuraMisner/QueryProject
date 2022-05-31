import sqlite3
import csv
from os import path
from sqlite3 import Error
from enum import Enum

# Storing schemas as global constants works fine for our purposes 
STATE_TABLE_SQL = """ 
    create table State (
        name        varchar(100) PRIMARY KEY,
        capital     varchar(100),
        population  integer
    ); """
COLLEGE_TABLE_SQL = """ 
    create table College (
        id          integer PRIMARY KEY AUTOINCREMENT,
        enrollment  integer,
        name        varchar(100),
        president   varchar(100),
        state       varchar(100),
        FOREIGN KEY(state) REFERENCES STATE(name)
    ); """


class query_type(Enum):
    STATE = 1
    STATES = 2
    STATE_COLLEGES = 3
    STATES_TOTAL_COLLEGES = 4
    STATES_TOTAL_ENROLLMENT = 5
    COLLEGE = 6
    COLLEGE_POPULATION_PERCENTAGE = 8
    LOAD_DATA = 9
    HELP = 10 
    QUIT = 11 


def create_table(conn, schema):
    """ Creates a table in the database with the given schema """
    cursor = conn.cursor()
    cursor.execute(schema)


def exists(conn, table_name):
    """ Checks if table exists in database """
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    status = cursor.fetchone()
    if status is None:
        return False
    else:
        return True

def table_empty(table,conn):
    """ Checks if table is empty """ 
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table}"); 
    result = cursor.fetchone()[0]
    return (result == 0)

def standup_database(path):
    """ Returns a connection to a SQLITE database, creating one if it does not already exist """
    conn = sqlite3.connect(path)

    if (not exists(conn, "College")):
        create_table(conn, COLLEGE_TABLE_SQL)

    if (not exists(conn, "State")):
        create_table(conn, STATE_TABLE_SQL)

    return conn


def get_table_cols(table_name, conn):
    """ Returns an (alphabetic) list of column names for a table """
    cursor = conn.cursor()
    cursor.row_factory = lambda cursor, row: row[0]  # Return each row as a single item, rather than a tuple with just one item (default)
    cursor.execute(f"SELECT c.name FROM pragma_table_info('{table_name}') c ORDER BY c.name ASC;")
    columns = cursor.fetchall()
    return list(filter(lambda s: s != "id", columns))

def empty_database(conn):
    """ Empties all data from database, but does not drop tables """ 
    cursor = conn.cursor() 
    cursor.execute("DELETE FROM College WHERE 1")
    cursor.execute("DELETE FROM State WHERE 1")
    conn.commit()

def load_data(path, table_name, conn):
    """ Populate table from data in csv file at provided path, assumes data is correct and in order with schema alphabetically """
    columns = get_table_cols(table_name, conn)
    comma_seperated_columns = ",".join(columns)
    cursor = conn.cursor()

    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            # We can assume our data is in the correct order because it's hardcoded files
            if table_name.lower() == "college":
                values = f"{row[0]},\"{row[1]}\",\"{row[2]}\",\"{row[3]}\""
            elif table_name.lower() == "state":
                values = f"\"{row[0]}\",\"{row[1]}\",{row[2]}"

            cursor.execute(f"INSERT INTO {table_name} ({comma_seperated_columns}) VALUES ({values})")

    conn.commit()


def do_query(query_t, args, conn):
    """ Determines which query to make based on args and queries DB, returns None if invalid args provided """ 
    if query_t == query_type.STATE:
        query = f"SELECT {args['property']} FROM STATE WHERE name LIKE \"{args['state_name']}\""
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    elif query_t == query_type.STATES:
        query = f"SELECT name FROM STATE"
    elif query_t == query_type.STATE_COLLEGES:
        query = f"SELECT name FROM COLLEGE WHERE state LIKE \"{args['state_name']}\""
    elif query_t == query_type.STATES_TOTAL_COLLEGES:
        query = f"SELECT COUNT(*) FROM COLLEGE WHERE state LIKE \"{args['state_name']}\""
    elif query_t == query_type.STATES_TOTAL_ENROLLMENT:
        query = f"SELECT SUM(enrollment) FROM COLLEGE WHERE state LIKE \"{args['state_name']}\""
    elif query_t == query_type.COLLEGE:
        query = f"SELECT {args['property']} FROM COLLEGE WHERE name LIKE \"{args['college_name']}\""
    elif query_t == query_type.COLLEGE_POPULATION_PERCENTAGE: 
        query = f"SELECT ROUND(((CAST(College.enrollment AS REAL) / State.population) * 100),2) FROM College JOIN State on College.state = State.name WHERE College.name LIKE \"{args['college_name']}\""
    else:
        return None

    cursor = conn.cursor()
    cursor.row_factory = lambda cursor, row: row[0]
    cursor.execute(query)
    return cursor.fetchall()

