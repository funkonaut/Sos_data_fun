"""Code to create the sql tables and schema for the SOS data this will be run once and most likely won't be needed as the schema is already in the github"""
import os
import meta_data as md


def create_data_table_schema(i,name): 
    """Create .sql schema file"""
    d = "sql"
    fn = f"create_{name}.sql"
    #Totals log is a bit different MAKE SURE THAT LAYOUT IS A UNIQUE KEY FOR TOTALS****
    if name == "totals_log":
        schema = f"CREATE TABLE {name.upper()} (\n    LAYOUT_CODE INT PRIMARY KEY NOT NULL,"
    else:
        schema = f"CREATE TABLE {name.upper()} (\n    FILING_NUM INT PRIMARY KEY NOT NULL,\n    LAYOUT_CODE INT NOT NULL,"
    for j,entry in enumerate(md.NAMES[i]):
        if (entry == "layout_code") | (entry == "filing_num") | (entry == "filler"): continue
        if md.DTYPES[i][j] == "N": dtype = "INT"
        elif "date" in entry: dtype = "DATE"
        else: dtype = "TEXT"
        schema += f"\n    {entry.upper()} {dtype},"
    #get rid of trailing , and add in );
    schema = schema[:-1]
    schema += "\n);"
    print(schema)
    with open(f"./{d}/{fn}", "w") as fh:
        fh.write(schema)
    run_schema(d,fn)

 
def run_schema(d,fn):
    """Run sql schema file to make data table"""
    os.system(f"psql -d Sos_data_fun -f ./{d}/{fn}")  
    print(f"Created sql table ran {fn}")
    return
 
   
def main():
    """Run over all tables in meta_data"""
    for i,name in enumerate(md.TABLE_NAMES):
        if name != "reserved": #Dont do reserved
            print(f"Now creating sql schema {name}")
            create_data_table_schema(i,name)

#To redo:
#dropdb Sos_data_fun
#createdb Sos_data_fun
#rm *.sql in ./sql
#run code
if __name__ == "__main__": 
   main() 
   #create_data_table_schema(4,"registered_agent_business")
