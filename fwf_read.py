"""The module to read in SOS fwf data"""

from itertools import accumulate
import re
import pandas as pd
import numpy as np
import meta_data


def read_data(fn: str) -> str:
    """The function to read in a txt file and strip newlines."""
    with open(fn,"r",encoding='cp1252') as fh:
        data = fh.read()
    data = data.replace("\n","")
    return data

#Maybe redo this so it defaults to 560 and if the first 2 arent 01-13 and 99 and the next 10 aren't digits find the width to make it so
def split_fw(data: str, n=560, daily=True) -> list:
    """The function to split a txt file according to a fixed width (n)."""
    l = []
    if daily:
        i = 0
        while i < len(data):
            if data[i:i+n].startswith("11"):#last entry is 560?
                n = 562
            elif re.match('\d{28}EDIT\s{6}(\s|(Vendor)|(Updated))',data[i:i+n])!=None:
                n = 260
            elif re.match('\d{20}ADD\s{8}',data[i:i+n])!=None:
                n = 252
            else:
                n = 560
            l.append(data[i:i+n])
            i += n
        return l               
    else:
        l = [data[i:i+n] for i in range(0, len(data), n)]
        return l

#Read sub fwfs according to specified fw from layout_code 
def read_multi_fwf(records: list) -> pd.DataFrame:
    """The function to split a list of fwf file according to metadata described
       in corp-bulkorder-layout.doc into a pandas dataframe"""
    #Read in that data
    dfs = []
    for record in records:
        #compute index from layout_code to use correct metadata
        layout_code = int(record[0:2])
        if layout_code == 99: continue#layout_code = 13
    
        #Split according to widths spec just makes it easier instead of typing in all start and end pos
        width = meta_data.WIDTHS[layout_code-1]
        bounds = list(accumulate(width, lambda a,b: a+b))
        col_widths = list(zip(bounds[0::1],bounds[1::1]))
        data_type = meta_data.DTYPES[layout_code-1]
       
        #Read all the entries according to meta_data and collect them as a list of dicts
        entry = []
        for w,dt in zip(col_widths,data_type): 
            data = record[w[0]:w[1]]
            if dt == "C": data = data.rstrip()
           # else: data = float(data) #FIX THIS TO GET CLEANER ENTRIES...
           #     if data == 0: data = np.nan
            entry.append(data)

        d = dict(zip(meta_data.NAMES[layout_code-1],entry)) 
        dfs.append(d)
    
    df = pd.DataFrame(dfs)
    return df

#TO DO: 
#Clean up "N" entries to display cleaner
#Link up df_meta and replace entries from each table as specified
if __name__ == "__main__":
    fn = "CD241120.txt"
#    fn = "CW211120.txt"
    l = split_fw(read_data(fn))
#    df = read_multi_fwf(split_fw(read_data(fn)))
    
