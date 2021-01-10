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
                print(f"{error}\n{data}\n{dt}\n{w}\n\n")
                data = np.nan
        entry.append(data)

    d = dict(zip(md.NAMES[layout_code-1],entry)) 
    return d


def main():
    directory = "../data/"
    for fn in os.listdir(directory):
        #log fn
        data = read_data(fn)
        df = split_read_combine(data)
        #dump to sheets
          #filter df by layout code and meta_data.NAMES[layout_code-1] 

#TO DO: 
#Link up df_meta and replace entries from each table as specified
#Convert dates to datetime objects
#Log record errors change prints to log
#Output to SQL table 
#Build SQL tables for each record entry number 01-12 and 99
if __name__ == "__main__":
    #main()  
    fn = "../data/CM000121_10.txt"
    data = read_data(fn)
    df = split_read_combine(data)
     








##Read sub fwfs according to specified fw from layout_code 
#def read_multi_fwf(records: list) -> pd.DataFrame:
#    """The function to split a list of fwf file according to metadata described
#       in corp-bulkorder-layout.doc into a pandas dataframe"""
#    #Read in that data
#    dfs = []
#    for record in records:
#        #compute index from layout_code to use correct metadata
#        layout_code = int(record[0:2])
#        if layout_code == 99: continue#layout_code = 13
#    
#        #Split according to widths spec just makes it easier instead of typing in all start and end pos
#        width = meta_data.WIDTHS[layout_code-1]
#        bounds = list(accumulate(width, lambda a,b: a+b))
#        col_widths = list(zip(bounds[0::1],bounds[1::1]))
#        data_type = meta_data.DTYPES[layout_code-1]
#       
#        #Read all the entries according to meta_data and collect them as a list of dicts
#        entry = []
#        for w,dt in zip(col_widths,data_type): 
#            data = record[w[0]:w[1]]
#            if dt == "C": data = data.rstrip()
#           # else: data = float(data) #FIX THIS TO GET CLEANER ENTRIES...
#           #     if data == 0: data = np.nan
#            entry.append(data)
#
#        d = dict(zip(meta_data.NAMES[layout_code-1],entry)) 
#        dfs.append(d)
#    
#    df = pd.DataFrame(dfs)
#    return df

##Maybe redo this so it defaults to 560 and if the first 2 arent 01-13 and 99 and the next 10 aren't digits find the width to make it so
#def split_fw(data: str, n=560, daily=True) -> list:
#    """The function to split a txt file according to a fixed width (n)."""
#    l = []
#    if daily:
#        i = 0
#        while i < len(data):
#            if data[i:i+n].startswith("11"):#last entry is 560?
#                n = 562
#            elif re.match('\d{28}EDIT\s{6}(\s|(Vendor)|(Updated))',data[i:i+n])!=None:
#                n = 260
#            elif re.match('\d{20}ADD\s{8}',data[i:i+n])!=None:
#                n = 252
#            else:
#                n = 560
#            l.append(data[i:i+n])
#            i += n
#        return l               
#    else:
#        l = [data[i:i+n] for i in range(0, len(data), n)]
#        return l

#def check_correct(data,i,n):
#    """The function to check if a fwf entry is the correct length"""
#    if data[i:i+n].endswith(" ") and re.match('((0[0-9])|(1[0-1]))',data[i:i+n]): #Assuming correct if it corresponds to layout file
#        return True
#    if re.match('99',data[i:i+n]) and data[i:i+n].endswith("0"):
#        return True
#    if re.match('12',data[i:i+n]) and re.match("[a-z]|[A-Z]|\s{1}", data[i+n-1:i+n]): #starts with 12 and ends with a alpha char
#        return True
##    if data[i:i+n].endswith(" ") and re.match('((0[0-9])|(1[0-2])|99)',data[i:i+n]): #Assuming correct if it corresponds to layout file (FIGURE OUT 12 and 99 WHAT TO DO!)
##        return True
#    return False


#def search_bounds(data,i,n):
#    """Look to find the correct bonds"""
#    if data[i:i+n].startswith(" "):
#        while not re.match('((0[0-9])|(1[0-2])|99)',data[i:i+n]): #make sure it starts right 
#            i = i+1
#   # else:
#   #     while check_correct(data,i,n) is False: # sometimes it doesnt end with a number will it sometimes end with a space and 0-12|99 but be wrong?
#   #         n = n-1
#   # 
#    return i,n
