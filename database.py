import os
from dotenv import load_dotenv
import psycopg2
import meta_data as md

load_dotenv()
local_dev = os.getenv("LOCAL_DEV") == "true"

def get_database_connection(local_dev=True):
    if local_dev:
        conn = psycopg2.connect(os.getenv("LOCAL_DATABASE_URL"))
    else:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn


def copy_from_file(conn, df, table):
    """
    Here we are going save the dataframe on disk as 
    a csv file, load the csv file  
    and use copy_from() to copy it to the table
    """
    # Save the dataframe to disk
    tmp_df = "./tmp_dataframe.csv"
    df.to_csv(tmp_df, index_label='id', header=False)
    f = open(tmp_df, 'r')
    cursor = conn.cursor()
    try:
        cursor.copy_from(f, table, sep=",")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        os.remove(tmp_df)
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("copy_from_file() done")
    cursor.close()
    os.remove(tmp_df)


def filter_df(df,layout_code):
#filter the read in dataframe for the record larout code
    return df.loc[df["layout_code"].eq(layout_code)][md.TABLE_NAMES[layout_code-1]]


def dump_df(df):
    conn = get_database_connection(local_dev=local_dev)
    for layout_code in df["layout_code"].unique():
        df_f = filter_df(df,layout_code) #filtered dataframe
        layout_code = int(layout_code)
        if layout_code == 99:
            layout_code = 13
        copy_from_file(conn, df_f, md.TABLE_NAMES[layout_code-1]) 
    

if __name__ == "__main__":
   #main()
   
