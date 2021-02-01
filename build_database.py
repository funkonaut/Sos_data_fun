"""
Code to build the SOS and TCAD database.
Builds schemas and popuates databases.
Runs quick search sql code and address normalization.
"""

import os
from dotenv import load_dotenv
import meta_data as md
import database as db
import update_TCAD_data as tcad
import fwf_read as fwf
from logger import logger

load_dotenv()
local_dev = os.getenv("LOCAL_DEV") == "true"

def create_data_table_schema(i,name): 
    """Create .sql schema file for SOS data."""
    d = "sql"
    fn = f"create_{name}.sql"
    #totals log is different everything else starts the same
    if name == "totals_log":
        schema = f"CREATE TABLE {name.upper()} (\n    LAYOUT_CODE TEXT,"
    else:
        schema = f"CREATE TABLE {name.upper()} (\n    FILING_NUM TEXT,\n    LAYOUT_CODE TEXT,"
    #go through tables and build schema based on meta_data.py
    for j,entry in enumerate(md.NAMES[i]):
        #not including filler and already have the other two
        if (entry == "layout_code") | (entry == "filing_num") | (entry == "filler"): continue
        #specify type
        if md.DTYPES[i][j] == "N": dtype = "NUMERIC"
        elif md.DTYPES[i][j] == "D": dtype = "DATE"
        else: dtype = "TEXT"

        schema += f"\n    {entry.upper()} {dtype},"
    
    #get rid of trailing , and add in );
    schema = schema[:-1]
    schema += "\n);"
    #create an index on filing_num for more efficient sql 
    if name != "totals_log":
        schema += f"\nCREATE INDEX ON {name.upper()}(FILING_NUM);"
    #write it out to a .sql file
    with open(f"./{d}/{fn}", "w") as fh:
        fh.write(schema)
    #actually do the thing
    run_schema(d,fn) 


def create_md_table_schema(col,table):
    """Create meta data schema for SOS."""
    d = "sql"
    fn = f"create_{table}.sql"
    schema = f"CREATE TABLE {table.upper()} ("
    for entry in col:
        schema += f"\n    {entry[0]} NUMERIC,"
        schema += f"\n    {entry[1]} TEXT,"
    #get rid of trailing , and add in );
    schema = schema[:-1]
    schema += "\n);"
    #write it out to a .sql file
    with open(f"./{d}/{fn}", "w") as fh:
        fh.write(schema)
    #actually do the thing
    run_schema(d,fn)
     
#THIS MIGHT NEED CHANGING WE STILL NEED TO LINK UP METADATA
def populate_meta_data_table(col, table):
    """Populate meta data for SOS."""
    conn = db.get_database_connection(local_dev=local_dev)
    for entry in col:
        df = md.df_meta[list(entry)].dropna()
        db.execute_values(conn,df,table)
        

def run_schema(d,fn):
    """Run sql schema file to make data table."""
    os.system(f"psql -d Sos_data_fun -f ./{d}/{fn}")  
    print(f"Created sql table ran {fn}")
    return
 

def create_tcad_schema():
    """Create TCAD property data schema."""
    d = "sql"
    table = "tcad"
    fn = f"create_{table}.sql"
    schema = f"CREATE TABLE {table} ("
    for name in md.tcad_prop_names:
        schema += f"\n    {name.upper()} TEXT,"
    #get rid of trailing , and add in );
    schema = schema[:-1]
    schema += "\n);"
    #write it out to a .sql file
    with open(f"./{d}/{fn}", "w") as fh:
        fh.write(schema)
    #actually do the thing
    run_schema(d,fn)


def create_sos_schema():    
    """Run over all tables in meta_data."""
    #1 indexed cycle thru [1,14) to index into meta data arrays
    for i in range(1,14): 
        #Create main database schema
        table = md.TABLE_NAMES[i-1] 
        #Dont do reserved
        if table != "reserved": 
            create_data_table_schema(i-1,table)

        #Create meta data schema and populate 
        col = md.COLS[i-1]
        table = md.MD_TABLE_NAMES[i-1]
        if col is not None:
            create_md_table_schema(col, table)
            populate_meta_data_table(col, table)

   
def main():
    #Build schema for SOS data
    logger.info("Creating SOS file schema")
    create_sos_schema()    
     
    #Populate SOS data
    logger.info("Running SOS file reads")
    fwf.main()

    #Create TCAD data schema and populate
    logger.info("Running TCAD file reads")
    #df = tcad.download_read()
    df = tcad.read_tcad()
    create_tcad_schema()
    conn = db.get_database_connection(local_dev=local_dev)
    db.execute_values(conn,df,"tcad")

    #Run normalization code for addresses
    logger.info("Running address normalization schema")
    run_schema("sql","create_normalized_addresses.sql") 

    #Run normalization code for addresses
    logger.info("Running index creation for names (biz/person")
    run_schema("sql","create_name_search_index.sql") 

#To redo:
#rm error.log
#dropdb Sos_data_fun
#createdb Sos_data_fun
#rm .sql in ./sql EXCEPT create_normalized_addresses.sql and create_name_search_index.sql
#createdb Sos_data_fun
#run code
if __name__ == "__main__": 
    main()
