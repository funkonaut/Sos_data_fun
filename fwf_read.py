"""The module to read in SOS fwf data into an SQL database"""
import os
from itertools import accumulate
import re
import pandas as pd
import numpy as np
import database as db 
import meta_data as md


def read_data(fn: str) -> str:
    """The function to read in a txt file and strip newlines."""
    with open(fn,"r",encoding='cp1252') as fh:
    #with open(fn,"r",encoding='utf-8') as fh:
        data = fh.read()
    return data

         
def split_read_combine(data):
    """The function to split the txt file into seperate entries 
       and then read them into a dict and combine them into a dataframe"""
    l = data.split('\n') #entries seperated by \n
    dfs = [] #array of dictionaries
    e = 0 
    for record in l:
       try: 
           d = read_multi_fwf(record)
           dfs.append(d)
       except Exception as error:
#           print(f"{error}\n{record}") 
           e += 1
    print(f"There were {e} errors check log for specifics")
    return pd.DataFrame(dfs) 
       

#Read sub fwfs according to specified fw from layout_code 
def read_multi_fwf(record):
    """The helper function to split a fwf file entry's fields according to metadata described
       in corp-bulkorder-layout.doc into a dictionary"""
    #Read in that data
    #compute index from layout_code to use correct metadata
    layout_code = int(record[0:2])
    if layout_code == 99: 
        layout_code = 13
         
    #Split according to widths spec just makes it easier instead of typing in all start and end pos
    width = md.WIDTHS[layout_code-1]
    bounds = list(accumulate(width, lambda a,b: a+b))
    col_widths = list(zip(bounds[0::1],bounds[1::1]))
    data_type = md.DTYPES[layout_code-1]
    
    #Read all the entries according to meta_data and collect them as a list of dicts
    entry = []
    for w,dt in zip(col_widths,data_type): 
        data = record[w[0]:w[1]]
        if dt == "C": data = data.rstrip()
        else:
            try: 
                data = data.lstrip('0') 
            except Exception as error:
                print(f"Left strip error: {error}\n{data}\n{dt}\n{w}\n\n")
                data = np.nan
        entry.append(data)

    d = dict(zip(md.NAMES[layout_code-1],entry)) 
    return d


def main():
    """Read in all files in data directory and dump them to a data table depeding on their layout_code"""
    directory = "../data/"
    for fn in os.listdir(directory):
        #log fn
        data = read_data(fn)
        df = split_read_combine(data)
        #link csv meta_data maybe this should be done elsewhere so as to conserve memory? when fetching data from sql
        db.dump_df(df)
        #dump to sheets
          #filter df by layout code and meta_data.NAMES[layout_code-1] 

#TO DO: 
#test this for one file 
#TEST DUMP to SQL table for one file

#Link up df_meta and replace entries from each table as specified
#Convert dates to datetime objects
#Log record errors change prints to log
#RUN CODE
if __name__ == "__main__":
    #main()  
    fn = "../data/CM000121_10.txt"
    data = read_data(fn)
    df = split_read_combine(data)
