import os
from dotenv import load_dotenv
import psycopg2
import meta_data as md
load_dotenv()

def get_database_connection(local_dev=True):
    if local_dev:
        conn = psycopg2.connect(os.getenv("LOCAL_DATABASE_URL"))
    else:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn


def dump_df():
#Dump the df to the correct sql table
     conn = get_database_connection()


def filter_df():
#filter the read in dataframe for the record larout code

