""" 
File has functions to login into SOS
web page and read the cookie for curling files
"""

import sys
import os
from datetime import datetime
from logger import logger 
import time
import shlex
import subprocess
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib3
from webdriver_manager.chrome import ChromeDriverManager
import meta_data as md

load_dotenv()

def init_wd():
    """Init selenium webdriver in headless mode."""
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(ChromeDriverManager().install(),options=options)

driver = init_wd()

def nav_url(browser,url=""):
    """Navigate to url.""" 
    try:
      time.sleep(1)
      browser.get(url)
    except Exception as e:
      logger.info(f"Could not navigate to url {e}")
      logger.error("Could not navigate to url")
      return 0
    logger.info("Successfully navigated to "+url)
    return 1


def build_cmd(dl)
    date = "1/29/2021"
    order = "1026032650002"
    cmd = f"""curl 'https://direct.sos.state.tx.us/{dl}' \
-H 'authority: direct.sos.state.tx.us' \
-H 'cache-control: max-age=0' \
-H 'sec-ch-ua: "Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"' \
-H 'sec-ch-ua-mobile: ?0' \
-H 'upgrade-insecure-requests: 1' \
-H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36' \
-H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
-H 'sec-fetch-site: none' \
-H 'sec-fetch-mode: navigate' \
-H 'sec-fetch-user: ?1' \
-H 'sec-fetch-dest: document' \
-H 'accept-language: en-US,en;q=0.9' \
-H 'cookie: ASPSESSIONIDAGASDSCB={cookie}; c%5Fclient%5Fid=80793825; c%5Fordering%5Fparty%5Femail=ap%40trla%2Eorg; c%5Fordering%5Fparty%5Ffax=956+968+8823; c%5Fordering%5Fparty%5Fphone=956+447+4800; c%5Fordering%5Fparty%5Fname=TEXAS+RIOGRANDE+LEGAL+AID%2C+INC%2E' \
  --compressed"""
    return cmd

def download_data(cookie):
    """Curl the weekly filing data."""
    dl = f"corp_bulkorder/corp_bulkorder.asp?submit=download&dn={order}&td={date}"
    cmd = build_cmd(dl)
    #figure out the actual donwload link
    out = subprocess.check_output(shlex.split(cmd))
    soup = BeautifulSoup(out, 'html.parser')
    for link in soup.find_all('a', href=True):
        dl = link['href']
    
    cmd = build_cmd(dl)
    out = subprocess.check_output(shlex.split(cmd))


def login_download():
    """Navigate login, scrape download url, dowload filing data."""
    logger.info(f"Logging in.")
    username = os.getenv("SOS_USERNAME")
    password = os.getenv("SOS_PASSWORD")
    try:
        driver.implicitly_wait(10)
        url = "https://direct.sos.state.tx.us/acct/acct-login.asp"
        nav_url(driver,url)
        #login
        driver.find_element_by_name("client_id").send_keys(username)
        driver.find_element_by_name("web_password").send_keys(password)
        driver.find_element_by_name("submit").click()
        logger.info("Successfully logged in.")
        #update billing info
        driver.implicitly_wait(3)
        driver.find_element_by_xpath("//select[@name='payment_type_id']/option[text()='Client Account']").click()
        driver.implicitly_wait(3)
        driver.find_element_by_name("Submit").click()
        driver.implicitly_wait(3)
        #get cookies for curl
        cookies = driver.get_cookies()
        print(cookies)
        cookie = cookies[-1]['value']#this is a bad assumpion
        download_data(cookie)
#        logger.info(f"Scraped TCAD data")
    except Exception as e:
        logger.info(f"Failed to login: {e}")
        logger.error(f"Failed to login: {e}")
#        sys.exit()
      

if __name__ == '__main__':
#    download_read()
#    print(read_tcad())
    login_download()
