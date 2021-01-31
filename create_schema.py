"""
Code to create the sql tables and schema for the SOS data this will be run once and 
most likely won't be needed once data is populated
as the schema is already in the github
"""
import os
from dotenv import load_dotenv
import meta_data as md
import database as db
import update_TCAD_data as tcad
import fwf_read as fwf

load_dotenv()
local_dev = os.getenv("LOCAL_DEV") == "true"

def create_data_table_schema(i,name): 
    """Create .sql schema file"""
    d = "sql"
    fn = f"create_{name}.sql"
    #Totals log is a bit different MAKE SURE THAT LAYOUT IS A UNIQUE KEY FOR TOTALS****
    if name == "totals_log":
        #schema = f"CREATE TABLE {name.upper()} (\n    LAYOUT_CODE INT PRIMARY KEY NOT NULL,"
        schema = f"CREATE TABLE {name.upper()} (\n    LAYOUT_CODE TEXT,"
    else:
        #schema = f"CREATE TABLE {name.upper()} (\n    FILING_NUM INT PRIMARY KEY NOT NULL,\n    LAYOUT_CODE INT NOT NULL,"
        schema = f"CREATE TABLE {name.upper()} (\n    FILING_NUM TEXT,\n    LAYOUT_CODE TEXT,"
    for j,entry in enumerate(md.NAMES[i]):
        if (entry == "layout_code") | (entry == "filing_num") | (entry == "filler"): continue

        if md.DTYPES[i][j] == "N": dtype = "NUMERIC" #This could be more space efficient*** but probably not a huge deal
        elif md.DTYPES[i][j] == "D": dtype = "DATE"
        else: dtype = "TEXT"

        #dtype = "TEXT"
        schema += f"\n    {entry.upper()} {dtype},"
    #get rid of trailing , and add in );
    schema = schema[:-1]
    schema += "\n);"
    if name != "totals_log":
        schema += f"\nCREATE INDEX ON {name.upper()}(FILING_NUM);"
    print(schema)
    with open(f"./{d}/{fn}", "w") as fh:
        fh.write(schema)
    run_schema(d,fn)


def create_md_table_schema(col,table):
    """Create .sql schema file"""
    d = "sql"
    fn = f"create_{table}.sql"
    schema = f"CREATE TABLE {table.upper()} ("
    for entry in col:
        schema += f"\n    {entry[0]} NUMERIC,"
        schema += f"\n    {entry[1]} TEXT,"
    #get rid of trailing , and add in );
    schema = schema[:-1]
    schema += "\n);"
    print(schema)
    with open(f"./{d}/{fn}", "w") as fh:
        fh.write(schema)
    run_schema(d,fn)
     

def populate_meta_data_table(col, table):
    conn = db.get_database_connection(local_dev=local_dev)
    for entry in col:
        df = md.df_meta[list(entry)].dropna()
        db.execute_values(conn,df,table)
        

def run_schema(d,fn):
    """Run sql schema file to make data table"""
    os.system(f"psql -d Sos_data_fun -f ./{d}/{fn}")  
    print(f"Created sql table ran {fn}")
    return
 

def create_tcad_schema():
    d = "sql"
    table = "tcad"
    fn = f"create_{table}.sql"
    schema = f"CREATE TABLE {table} ("
    for name in md.tcad_prop_names:
        schema += f"\n    {name.upper()} TEXT,"
    #get rid of trailing , and add in );
    schema = schema[:-1]
    schema += "\n);"
    print(schema)
    with open(f"./{d}/{fn}", "w") as fh:
        fh.write(schema)
    run_schema(d,fn)
    

   
def main():
    """Run over all tables in meta_data"""
    for i in range(1,14): #1 indexed cycle thru [1,14) to index into meta data arrays
        #Create main database schema
        table = md.TABLE_NAMES[i-1]
        if table != "reserved": #Dont do reserved
            print(f"Now creating sql schema {table}")
            create_data_table_schema(i-1,table)

        #Create meta data schema and populate 
        col = md.COLS[i-1]
        table = md.MD_TABLE_NAMES[i-1]
        if col is not None:
            create_md_table_schema(col, table)
            populate_meta_data_table(col, table)
         
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


#To redo:
#rm error.log
#dropdb Sos_data_fun
#createdb Sos_data_fun
#rm *.sql in ./sql
#run code
if __name__ == "__main__": 
#    main()
    df = tcad.read_tcad()
    create_tcad_schema()
    conn = db.get_database_connection(local_dev=local_dev)
    db.execute_values(conn,df,"tcad")
