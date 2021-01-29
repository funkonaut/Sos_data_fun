import os
from os.path import isfile
import sys
import logging
from dotenv import load_dotenv
import pandas as pd
import geopandas as gpd
from sodapy import Socrata
import gsheet
from pandas_profiling import ProfileReport
from ExploriPy import EDA
import numpy as np

#Global .env
load_dotenv()
TOKEN = "mvlgSH4w9oU80VMsFQy9GbMss"

#Logger
logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.INFO)


def read_tcad(fn='../data/TCAD/'):
    #Appraisal data for Travis county: https://www.traviscad.org/reports-request/
    col_specs = [(12,17),(2608,2609),(2033,2058),(2731,2741),(2741,2751),(2751,2761),(1745,1795),(1695,1745),(1675,1685),(1659,1675),(1149,1404),(1915,1930),(1686,1695),(546,596),(0,12),(596, 608),(608,678),(4459,4474),(1039,1049),(1049,1099),(1099,1109),(1109,1139),(1139,1149),(4475,4479),(693,753),(753,813),(813,873),(873,923),(923,974),(978,983),(4135,4175)]
    df_tcad = pd.read_fwf(fn+'PROP.TXT',col_specs,encoding = "ISO-8859-1")
    df_tcad.columns = ['type','hs','deed','code','code2','code3','lot','block','sub_div','acre','desc','value','hood','geo_id','prop_id', 'py_owner_i','prop_owner','st_number','prefix','st_name','suffix','city','zip','unit_num','mail_add_1','mail_add_2','mail_add_3','mail_city','mail_state','mail_zip','DBA']
    #Improvement data (type and property ID
#    col_specs =[(38,63),(0,12)]
#    df_units = pd.read_fwf(fn+'IMP_INFO.TXT',col_specs,encoding = "ISO-8859-1")
#    df_units.columns = ['type1','prop_id']
#    #Merge
#    df_tcad = df_tcad.merge(df_units,on='prop_id',how="outer")
    logger.info(f"Successfully read TCAD data")
    return df_tcad 


def type_meta(df,meta):
    """Convert df to meta data types"""
    for i in meta['columns']:
        col = i['fieldName']
        dtype = i['dataTypeName']
        if dtype == "text":
            df[col] = df[col].astype(str)
        if dtype == "number":
            df[col] = pd.to_numeric(df[col])#errors='coerce'|'ignore'
        if dtype == "calendar_date":
            df[col] = pd.to_datetime(df[col]).apply(lambda x: x.date())
        if dtype == "url":
            df[col] = df[col].apply(lambda x: x["url"] if x is not np.nan else np.nan)
#        if dtype == "location"
#            df[i['fieldName']] 
    return df
    

def read_oa(fn="6wtj-zbtb"):
    client = Socrata("data.austintexas.gov", TOKEN)
    results = list(client.get_all(fn))
    meta =  client.get_metadata(fn)
    df = pd.DataFrame.from_records(results)
    df = type_meta(df,meta)
    return df

    
def read_oa_list():
    fns = ["6wtj-zbtb", "afwp-v695"]
    #maybe change to df list instead of dict?
    names = {"Code complaint cases":pd.DataFrame(), "Code complaint events":pd.DataFrame()}#"Covid Complaints":pd.DataFrame(),
    for fn, name in zip(fns, names.keys()):
        logger.info(f"Reading {name}")
        df = read_oa(fn)
        names[name] = df     
        logger.info(f"Read {name}")
    return names        


def read_local_data():
    """Read all files in ../data try csv try json try shp"""
    d = "../data/"
    dfs = []
    for fn in os.listdir(d):
        if isfile(d+fn):
            if fn.endswith(".csv"):
                df = pd.read_csv(d+fn)
            if fn.endswith(".json"): 
                df = pd.read_json(d+fn)  
#            if fn.endswith(".shp"):
#                df = gpd.read_file(d+fn)
            dfs.append(df)
    return dfs 


def read_gsheet_data():
    #Do we want to read in other data?
    ws = [("Contact_data",0)]
    dfs = []
    client = gsheet.init_sheets()
    for w in ws: 
        sheet = gsheet.open_sheet(client, w[0], w[1])
        df = gsheet.read_data(sheet)
        dfs.append(df)

    return dfs


#COA city council districts map
#gdfdist = geopandas.read_file('../data_laundry/districts/geo_export_74417697-1c4c-4575-bf46-90c0ce62509c.shp')
#Social Vulnerability heat map
#gdf_sv = geopandas.read_file('../data_laundry/A2SI_SVI/A2SI_SVI.shp')
if __name__ == "__main__":
    dfs_oa = read_oa_list() #comment out when debuggin locally so as to not hit their server too much
    dfs_ld = read_local_data()
    dfs_gs = read_gsheet_data()
    df_tcad = read_tcad()

    try: #local or api
        df_cc = dfs_oa['Code complaint cases']
        df_ce = dfs_oa['Code complaint events']
    except:
        df_cc = dfs_ld[1]
        df_ce = dfs_ld[2]
    df_ll = dfs_ld[0]
    #clean up landlord data
    df_ll.drop(["Unnamed: 0"],axis=1,inplace=True)
    df_cd = dfs_gs[0]

    df_cc.to_csv("Code complaint cases.csv")
    df_ce.to_csv("Code complaint events.csv")
    #FIGURE OUT WHY TYPE CONVERSION IS NOT WORKING MAYBE JUST PULL IT DOWN HERE*

    #Time deltas
    df_cc['closed-open'] = df_cc['closed_date'] - df_cc['opened_date']
    df_cc['updated-open'] = df_cc['date_updated'] - df_cc['opened_date']
     
    #Of interest active cases that are over due 
    #Link to tcad data persist cases
    df_tcad_cc = df_tcad.merge(df_cc, left_on="geo_id", right_on="parcelid",how="right")
    df_tcl = df_tcad_cc.merge(df_ll,right_on="Property Index Number",left_on="prop_id",how="outer")
    
    df_active =  df_tcl.loc[(df_tcl['status']=="Active")]
    df_active["location"]=df_active["location"].astype(str)
#    df_active['repeatoffenderrelated'].replace('nan','No',inplace=True) 
#    df_active["parcelid"].replace('',np.nan,inplace=True) #This might be something other then ''
#    df_active.dropna(inplace=True) 
#    feats = ['priority','status','zip_code','opened_date','closed_date','department','case_type','inspector','shorttermrentalrelated','date_updated','closed-open','updated-open','repeatoffenderrelated']
    #profile = ProfileReport(df_cc[feats], title="Pandas Profiling Report")
    #profile.to_widgets()
#match reported by with eviction data*
    eda = EDA(df_active.drop(["updated-open","closed-open"],axis=1),title="Code Case Details")
#    eda = EDA(df_cc[feats],title="Code Case Details")
    eda.TargetAnalysis('repeatoffenderrelated')

