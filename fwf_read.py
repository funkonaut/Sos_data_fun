"""
The module to read in SOS fwf data into an SQL database.
"""

import os
import sys
from datetime import datetime, date
from itertools import accumulate
from logger import logger 
import re
import pandas as pd
import numpy as np
import database as db 
import meta_data as md
import clean_up as cu


def read_data(fn: str) -> str:
    """Read in a txt file and strip newlines."""
    with open(fn,"r",encoding='Latin-1') as fh:
        data = fh.read()
    return data

     
def convert_date(data):
    """Convert a data entry (YYYYDDMM) to a date."""
    return datetime.strptime(data, '%Y%m%d').date()


def split_read_combine(data):
    """Split/read entries into a dict/combine them into a dataframe."""
    l = data.split('\n') #entries delimited by \n
    dfs = [] #array of dictionaries
    e = 0 
    fw_e = 0
    for record in l:
        try: 
            d,fw_e = read_multi_fwf(record,fw_e)
            dfs.append(d)
        except Exception as error:
            logger.error(f"{error}\n'{record}'") 
            e += 1
    logger.info(f"There were {e} record read errors check log for specifics")
    logger.info(f"There were {fw_e} fixed width entry (type) errors check log for specifics")
    return pd.DataFrame(dfs) 
       

#Read sub fwfs according to specified fw from layout_code 
def read_multi_fwf(record,fw_e):
    """Split a fwf file entry's fields according to metadata described in corp-bulkorder-layout.doc into a dictionary."""
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
        if dt == "C": #Character type
            data = data.rstrip() #left justified space padded
            data = data.upper() #TEXT data should be uppercased do we want to strip punctuation too?
        elif dt == "D": #Date type
            try:
                data = data.lstrip('0') #right justified 0 padded
                data = convert_date(data)                 
            except Exception as error:
                data = data.strip()
                if data != "":
                    fw_e += 1
                    logger.error(f"{error}: Could not convert {data} to date")
                data = None
        else:# N (numeric type)
            try: 
                data = data.lstrip('0') 
                data = int(data)
            except Exception as error:
                data = data.strip()
                if data != "":
                    fw_e += 1
                    logger.error(f"{error}: Could not convert {data} to int")
                data = None
        entry.append(data)

    d = dict(zip(md.NAMES[layout_code-1],entry)) 
    return d,fw_e


def main():
    """Read in all files in data directory and dump them to a data table depeding on their layout_code."""
    directory = "../data/"
    logger.info(f"Reading and populating SOS data")
    for fn in os.listdir(directory):
        if fn.endswith(".txt"):#Only read in txt files
            logger.info(f"Reading in file: {fn}")
            data = read_data(directory + fn)
            df = split_read_combine(data)
            logger.info(f"Read in file: {fn}")
            db.dump_df(df) 
#also link meta_data and types?
#KEEPING DELETE_LOG records
#    cu.delete_records()
    logger.info(f"Read and populated SOS data")

if __name__ == "__main__":
    main()  
