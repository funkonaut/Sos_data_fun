"""
PostgreSQL database related functions. 
"""

import os
import sys
from io import StringIO
from logger import logger
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2 import sql
import psycopg2.extras as extras
import meta_data as md

load_dotenv()
local_dev = os.getenv("LOCAL_DEV") == "true"


def get_database_connection(local_dev=True):
    """Connection to PSQL DB."""
    if local_dev:
        conn = psycopg2.connect(os.getenv("LOCAL_DATABASE_URL"))
    else:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn


def execute_values(conn, df, table):
    """Using psycopg2.extras.execute_values() to insert the dataframe."""
    #Convert nans to None for SQL and clean up
    df = df.where(pd.notnull(df), None)
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL quert to execute
    query  = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error {table}: {error}")
        print(f"Error {table}: {error}")
        conn.rollback()
        cursor.close()
        return 1
    logger.info(f"execute_values for {table} done")
    cursor.close()


def filter_df(df,layout_code):
    """Filter only layout_code entries in dataframe."""
    #totals_log is the 12th entry in meta_data.py array NAMES
    if layout_code == 99:
        cols = md.NAMES[13-1]
    else:
        cols = md.NAMES[layout_code-1]

    if "filler" in cols:    
        cols.remove("filler")    
   
    return df.loc[df["layout_code"].eq(layout_code)][cols]


def dump_df(df):
    """Insert all entries into their layout_code tables."""
    conn = get_database_connection(local_dev=local_dev)
    #make sure type is consistant
    df['layout_code'] = df['layout_code'].astype(int)
    for layout_code in df["layout_code"].unique():
        df_f = filter_df(df,layout_code) #filtered dataframe
        if layout_code == 99:
            table = md.TABLE_NAMES[13-1]
        else:
            table = md.TABLE_NAMES[layout_code-1]
        execute_values(conn, df_f, table) 


def dump_to_df(conn,table):
    """Read all entries from table into a dataframe."""
    df = pd.read_sql_query('SELECT * FROM "%s"'%(table),con=conn)
    return df


