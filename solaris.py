from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import numpy as np
import pyodbc
import pandas as pd
import string
import calendar
import random
from sqlalchemy import create_engine
import urllib
import json

def get_json(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    json_elem = json.loads(driver.find_element(By.CSS_SELECTOR, "script[type='application/ld+json']").get_attribute('innerHTML'))
    print(json_elem['name'])
    print(json_elem['sku'])
    notPreOrder = True
    for f in json_elem['offers']:
        if 'EARLY' in f['sku']:
            print('This is a preorder item')
            notPreOrder = False
    if notPreOrder:
        for f in json_elem['offers']:
            if 'InStock' in f['availability']:
                print('InStock')
            if 'OutOfStock' in f['availability']:
                print('OutOfStock')
            print(f['price'])
            print(f['priceCurrency'])
            if 'NewCondition' in f['itemCondition']:
                print('NewCondition')
            if 'UsedCondition' in f['itemCondition']:
                print('UsedCondition')
    driver.close()

get_json('https://solarisjapan.com/products/azur-lane-baltimore-finish-line-flagbearer-ver-1-7-apex?oid=167005&qid=5e86ce4e4391684bac002bd0d00beae2#')
print()
get_json('https://solarisjapan.com/products/azur-lane-prinz-eugen-final-lap-ver-1-7-apex?oid=202251&qid=dfe9106f764399ac3fe00cdc008b31b5')