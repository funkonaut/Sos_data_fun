""" 
File has functions to update TCAD data from the traviscad.org
web page and read the data into a pandas dataframe.
"""

import sys
import os
from datetime import datetime
from logger import logger 
import time
import numpy as np
import pandas as pd
import selenium
from selenium import webdriver
import urllib3
from webdriver_manager.chrome import ChromeDriverManager
import meta_data as md


def init_wd():
    """Init selenium webdriver in headless mode."""
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(ChromeDriverManager().install(),options=options)


def nav_url(browser,url=""):
    """Navigate to url.""" 
    try:
      time.sleep(1)
      browser.get(url)
    except Exception as e:
      logger.info("Could not navigate to url")
      logger.error("Could not navigate to url")
      return 0
    logger.info("Successfully navigated to "+url)
    return 1


def download_data(url_down):
    """Curl the TCAD data into ./data/TCAD"""
    date = str(datetime.date(datetime.now()))
    fn = 'tcad' + date + '.zip'
    od = '../data/TCAD'
    os.system('curl '+url_down+' -o '+fn)
    os.system('unzip '+fn+' -d '+od)
    os.system('rm '+fn) 


def scrape_url(url="https://www.traviscad.org/reports-request/"):
    """Navigate, scrape download url, dowload TCAD data."""
    logger.info(f"Scraping TCAD data")
    try:
        browser = init_wd()
        #wait 10 seconds when doing a find_element
        browser.implicitly_wait(10)
        nav_url(browser,url)
        link = browser.find_element_by_link_text('TCAD APPRAISAL ROLL EXPORT')
        url_down = link.get_attribute("href")
        logger.info("Successfully fetched link "+url_down)
        download_data(url_down)
        logger.info(f"Scraped TCAD data")
    except Exception as e:
        logger.error("Failed to fetch link")
        sys.exit()
      

def read_tcad(fn='../data/TCAD/'):
    """Read TCAD property data into a dataframe."""
    logger.info(f"Reading TCAD data")
    df_tcad = pd.read_fwf(fn+'PROP.TXT', md.tcad_prop_w, encoding = "ISO-8859-1")
    df_tcad.columns = md.tcad_prop_names
    ##Clean up entries
    df_tcad = df_tcad.apply(lambda x: x.astype(str).str.upper())
    ##Upper case all text strip punctuation?
    ##Convert to nan will convert to None in execute_values()
    df_tcad = df_tcad.replace("NAN",np.nan) 
    logger.info(f"Successfully read TCAD data")
    return df_tcad 


def download_read():
    """Download and read TCAD data."""
    scrape_url()
    df_tcad = read_tcad() 
    return df_tcad


if __name__ == '__main__':
#    download_read()
    print(read_tcad())
