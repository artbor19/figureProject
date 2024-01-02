from Tools.scripts.dutree import display
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

def get_JAN_amiami():
    figures = []
    driver = webdriver.Chrome()
    driver.get("https://www.amiami.com")
    time.sleep(2)
    assert "AmiAmi" in driver.title
    time.sleep(2)
    menu = driver.find_element(By.ID, 'mega-dropdown')
    time.sleep(0.25)
    menu_items = driver.find_elements(By.CLASS_NAME, 'mega-dropdown-menu__list__list-item')
    time.sleep(0.25)
    figures_home = None
    for m in menu_items:
        if 'Figures' in m.text:
            m.click()
            sub_list = m.find_element(By.ID, 'mega-dropdown-menu-category01')
            sub_categories = sub_list.find_elements(By.TAG_NAME, 'li')
            for s in sub_categories:
                if 'Bishoujo Figures' in s.text:
                    figures_home = s
                    break;
    figures_home.click()
    time.sleep(2)
    newly_added = driver.find_element(By.CLASS_NAME, 'newly-added-items__list')
    figure_links = newly_added.find_elements(By.TAG_NAME, 'a')
    links = []
    for f in figure_links:
        links.append(f.get_attribute('href'))
    for l in links:
        figure = []
        driver.get(l)
        time.sleep(3)
        figure_title = driver.find_element(By.CLASS_NAME, 'item-detail__section-title')
        figure.append(figure_title.text)
        jp_price = driver.find_element(By.CLASS_NAME, 'item-detail__price_selling-price')
        figure.append(jp_price.text)
        currency_price = driver.find_element(By.CLASS_NAME, 'item-detail__currency')
        local_price = (currency_price.text.split('\n')[0])
        figure.append(local_price.replace('(appx. ', ''))
        about_all = driver.find_elements(By.CLASS_NAME, 'item-about__data')
        for a in about_all:
            if 'JAN code' in a.text:
                figure.append(a.text.split('JAN code')[1].strip())
        driver.back()
        time.sleep(2)
        print(figure)
        figures.append(figure)
    driver.close()

#get_JAN_amiami()

def amiami_lookup(jan):
    figures = []
    driver = webdriver.Chrome()
    driver.get("https://www.amiami.com")
    time.sleep(2)
    assert "AmiAmi" in driver.title
    time.sleep(2)
    searchBar = driver.find_element(By.ID, 'searchBoxInput')
    searchButton = driver.find_element(By.CLASS_NAME, 'search-box__button')
    searchBar.send_keys(jan)
    time.sleep(0.25)
    searchButton.click()
    time.sleep(5)

    results = driver.find_element(By.CLASS_NAME, 'new-items__inner')
    figure_links = results.find_elements(By.TAG_NAME, 'a')
    links = []
    for f in figure_links:
        links.append(f.get_attribute('href'))
    for l in links:
        figure = []
        driver.get(l)
        time.sleep(3)
        figure_title = driver.find_element(By.CLASS_NAME, 'item-detail__section-title')
        figure.append(figure_title.text)
        jp_price = driver.find_element(By.CLASS_NAME, 'item-detail__price_selling-price')
        figure.append(jp_price.text)
        currency_price = driver.find_element(By.CLASS_NAME, 'item-detail__currency')
        local_price = (currency_price.text.split('\n')[0])
        figure.append(local_price.replace('(appx. ', ''))
        about_all = driver.find_elements(By.CLASS_NAME, 'item-about__data')
        for a in about_all:
            if 'JAN code' in a.text:
                figure.append(a.text.split('JAN code')[1].strip())
        driver.back()
        time.sleep(2)
        print(figure)
        figures.append(figure)
    driver.close()

#amiami_lookup('4595123918180')

def parse_all_page(driver, df):
    matching_params = driver.find_element(By.CLASS_NAME, 'new-items__inner')
    figure_general_box = matching_params.find_elements(By.CLASS_NAME, 'newly-added-items__item.nomore')
    for f in figure_general_box:

        figure = {
            'jan_code': None,
            'store_id ': 1,
            'currency_code': None,
            'price': 0,
            'is_preorder': 0,
            'is_available': 1,
            'is_limited_edition': 0,
            'url': None
        }

        limited_check = f.find_element(By.CLASS_NAME,
                                       'newly-added-items__item__tag-list__line.newly-added-items__item__tag-list__line_limited')
        if 'Limited' in limited_check.text:
            figure['is_limited_edition'] = 1

        preOrder_check = f.find_element(By.CLASS_NAME,
                                        'newly-added-items__item__tag-list__item.newly-added-items__item__tag-list__item_preorder')
        if 'Pre-order' in preOrder_check.text:
            figure['is_preorder'] = 1

        currency_check = f.find_element(By.CLASS_NAME, 'newly-added-items__item__price_state_currency')
        figure['currency_code'] = currency_check.text

        url_check = f.find_element(By.TAG_NAME, 'a')
        figure['url'] = url_check.get_attribute('href')

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.5)
        driver.get(figure['url'])
        time.sleep(3)

        jp_price = driver.find_element(By.CLASS_NAME, 'item-detail__price_selling-price')
        figure['price'] = float(jp_price.text.replace('JPY', '').replace(',', ''))
        about_all = driver.find_elements(By.CLASS_NAME, 'item-about__data')
        for a in about_all:
            if 'JAN code' in a.text:
                figure['jan_code'] = a.text.split('JAN code')[1].strip()

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.5)

        df = pd.concat([df, pd.DataFrame([figure])], ignore_index=True)
    return df


def new_listing_table():
    newListingDF = pd.DataFrame()

    driver = webdriver.Chrome()
    driver.get(
        "https://www.amiami.com/eng/search/list/?s_st_list_preorder_available=1&s_cate2=459&s_st_list_newitem_available=1")
    time.sleep(2)
    assert "AmiAmi" in driver.title
    time.sleep(2)

    figure_df = pd.DataFrame()

    figure_df = parse_all_page(driver, figure_df)
    time.sleep(3)
    # for i in range(4):
    # nextPage = driver.find_element(By.CLASS_NAME, 'pager__next')
    # nextPage.click()
    # time.sleep(3)
    # figure_df = parse_all_page(driver, figure_df)
    display(figure_df)
    driver.close()

    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-QLGCSG7;DATABASE=figure_tracker;Trusted_Connection=yes;Encrypt=no;")
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params))
    figure_df.to_sql('NewListings', engine, if_exists='append', index=False)


new_listing_table()

