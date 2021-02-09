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
import fwf_read as fwf

load_dotenv()
local_dev = os.getenv("LOCAL_DEV") == "true"


def get_database_connection(local_dev=True):
    """Connection to PSQL DB."""
    if local_dev:
        conn = psycopg2.connect(os.getenv("LOCAL_DATABASE_URL"))
    else:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn

conn = get_database_connection(local_dev=local_dev)
cursor = conn.cursor()


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


def delete_log(df_del):
    """Delete records for df_del["filing number"] from all tables."""
    skip = ["reserved", "totals_log", "delete_all_log"]
    tables = [table for table in md.TABLE_NAMES if table not in skip]
    for table in tables:
        for i,row in df_del.iterrows():
            filing_del = row["filing_num"]
            cursor.execute(sql.SQL("DELETE FROM {} WHERE filing_num=%s;").format(sql.Identifier(table)),[str(int(filing_del))])
        conn.commit()
        logger.info(f"Removed delete_all_log entries for {table}")
    return



#Takes in weekly dump from SOS and updates the database maybe put in fwf_read
#is address ever updated without a mster filing?
#test this? read meta data more!
def update_database(fn):
    """Read in one weekly update file {fn} and add it to the database"""
    fn = "../data/weekly_updates/"+fn
    data = fwf.read_data(fn)
    df = fwf.split_read_combine(data)
    df_2 = filter_df(df,2)
    #search and replace filing number
    delete_log(df_2)
    dump_df(df)
    return


def dump_to_df(conn,table):
    """Read all entries from table into a dataframe."""
    df = pd.read_sql_query('SELECT * FROM "%s"'%(table),con=conn)
    return df


if __name__=="__main__":
#delete logs
#    df_del = dump_to_df(conn, "delete_all_log")
#    delete_log(df_del)
    update_database("CW030121.txt")
