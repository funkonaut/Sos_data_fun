"""
Functions to clean up the data as specified by the data.
"""

import os
import sys
from logger import logger
from dotenv import load_dotenv
import pandas as pd
from psycopg2 import sql
import meta_data as md
import database as db


def delete_records():
    """Delete records in delete_log table from other tables."""
    conn = db.get_database_connection(local_dev=local_dev)     
    cursor = conn.cursor()
    df_del = db.dump_to_df(conn, "delete_all_log")
    skip = ["reserved", "totals_log", "delete_all_log"] 
    tables = [table for table in md.TABLE_NAMES if table not in skip]
    for table in tables:
        for i,row in df_del.iterrows():
            filing_del = row["filing_num"]            
            cursor.execute(sql.SQL("DELETE FROM {} WHERE filing_num=%s;").format(sql.Identifier(table)),[filing_del])
        conn.commit()    
        logger.info(f"Removed delete_all_log entries for {table}")
    return


#Takes in weekly dump from SOS and updates the database maybe put in fwf_read
def update_database():
    #completely replace the database table with a new dataframe
    return

