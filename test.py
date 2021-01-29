import pandas as pd

def unique_compare(df1,df2): 
    for col1,col2 in zip(df1.columns,df2.columns):
        if len(df1[col1].unique()) != len(df1[col1].unique()):
            print(f"Discrepency in Unique entries in {col1} and {col2}")
            return 0
        else:
            return 1

