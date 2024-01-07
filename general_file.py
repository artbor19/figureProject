#AmiAmi data mining branch

from tabulate import tabulate
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


def check_used(jan):
    jan_list = []
    conn = pyodbc.connect('Driver={SQL Server};' 'Server=DESKTOP-QLGCSG7;' 'Database=figure_tracker;' 'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute("SELECT jan_code FROM NewListings WHERE jan_code = '{}'".format(jan))
    for row in cursor.fetchall():
        jan_list.append(row[0])
    conn.close()
    if len(jan_list) > 0:
        return True
    else:
        return False


def check_new(jan):
    jan_list = []
    conn = pyodbc.connect('Driver={SQL Server};' 'Server=DESKTOP-QLGCSG7;' 'Database=figure_tracker;' 'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute("SELECT jan_code FROM NewListings WHERE jan_code = '{}'".format(jan))
    for row in cursor.fetchall():
        jan_list.append(row[0])
    conn.close()
    if len(jan_list) > 0:
        return True
    else:
        return False


def amiami_lookup(jan):
    new_exists = check_new(jan)
    preowned_exists = check_used(jan)

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
    figure_boxes = results.find_elements(By.CLASS_NAME, 'newly-added-items__item.nomore')

    for f in figure_boxes:

        check_preowned = f.find_element(By.CLASS_NAME,
                                        'newly-added-items__item__tag-list__item.newly-added-items__item__tag-list__item_preowned')
        if 'Pre-owned' in check_preowned.text:
            figure = {
                'jan_code': jan,
                'store_id ': 1,
                'currency_code': None,
                'price': 0,
                'is_available': 1,
                'is_limited_edition': 0,
                'condition': None,
                'url': None
            }

            if preowned_exists:
                used_df = pd.DataFrame()
                print('figure(s) already in table updating')

                limited_check = f.find_element(By.CLASS_NAME,
                                               'newly-added-items__item__tag-list__line.newly-added-items__item__tag-list__line_limited')
                if 'Limited' in limited_check.text:
                    print('found limited preowned')
                    figure['is_limited_edition'] = 1

                    availability_check = f.find_element(By.CLASS_NAME, 'newly-added-items__item__tag-list__item')
                    if 'Order Closed' in limited_check.text:
                        figure['is_available'] = 0

                    currency_check = f.find_element(By.CLASS_NAME, 'newly-added-items__item__price_state_currency')
                    figure['currency_code'] = currency_check.text

                    url_check = f.find_element(By.TAG_NAME, 'a')
                    figure['url'] = url_check.get_attribute('href')

                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(0.5)
                    driver.get(figure['url'])
                    time.sleep(3)

                    conn = pyodbc.connect(
                        'Driver={SQL Server};' 'Server=DESKTOP-QLGCSG7;' 'Database=figure_tracker;' 'Trusted_Connection=yes;')
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM PreownedListings WHERE jan_code = '{}' AND is_limited_edition = 1".format(
                            figure['jan_code']))
                    cursor.commit()
                    cursor.close()

                    jp_price = driver.find_element(By.CLASS_NAME, 'item-detail__price_selling-price')
                    figure['price'] = float(jp_price.text.replace('JPY', '').replace(',', ''))
                    about_all = driver.find_elements(By.CLASS_NAME, 'item-about__data')

                    figure['condition'] = 'Item:' + \
                                          driver.find_element(By.CLASS_NAME, 'item-detail__section-title').text.split(
                                              ')')[0].split('/')[0].split(':')[1]

                    try:
                        more_choices = driver.find_element(By.CLASS_NAME, 'buying-choices-contents')
                        other_listings = more_choices.find_elements(By.CLASS_NAME, 'buying-choices-contents__list')
                        for o in other_listings:
                            sub_figure = {
                                'jan_code': figure['jan_code'],
                                'store_id ': 1,
                                'currency_code': figure['currency_code'],
                                'price': 0,
                                'is_available': 1,
                                'is_limited_edition': figure['is_limited_edition'],
                                'condition': None,
                                'url': figure['url']
                            }

                            other_listing = o.find_element(By.CLASS_NAME,
                                                           'buying-choices-contents__list_price').text.split('\n')
                            sub_figure['price'] = float(other_listing[0].replace(',', '').replace('JPY', ''))
                            sub_figure['condition'] = other_listing[1].replace('Condition', '').split('Box')[0].strip()
                            used_df = pd.concat([used_df, pd.DataFrame([sub_figure])], ignore_index=True)

                    except:
                        None

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(0.5)

                    used_df = pd.concat([used_df, pd.DataFrame([figure])], ignore_index=True)

                    params = urllib.parse.quote_plus(
                        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-QLGCSG7;DATABASE=figure_tracker;Trusted_Connection=yes;Encrypt=no;")
                    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params))
                    used_df.to_sql('PreownedListings', engine, if_exists='append', index=False)

                #####
                else:

                    availability_check = f.find_element(By.CLASS_NAME, 'newly-added-items__item__tag-list__item')
                    if 'Order Closed' in limited_check.text:
                        figure['is_available'] = 0

                    currency_check = f.find_element(By.CLASS_NAME, 'newly-added-items__item__price_state_currency')
                    figure['currency_code'] = currency_check.text

                    url_check = f.find_element(By.TAG_NAME, 'a')
                    figure['url'] = url_check.get_attribute('href')

                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(0.5)
                    driver.get(figure['url'])
                    time.sleep(3)

                    conn = pyodbc.connect(
                        'Driver={SQL Server};' 'Server=DESKTOP-QLGCSG7;' 'Database=figure_tracker;' 'Trusted_Connection=yes;')
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM PreownedListings WHERE jan_code = '{}' AND is_limited_edition = 0".format(
                            figure['jan_code']))
                    cursor.commit()
                    cursor.close()

                    jp_price = driver.find_element(By.CLASS_NAME, 'item-detail__price_selling-price')
                    figure['price'] = float(jp_price.text.replace('JPY', '').replace(',', ''))
                    about_all = driver.find_elements(By.CLASS_NAME, 'item-about__data')

                    figure['condition'] = 'Item:' + \
                                          driver.find_element(By.CLASS_NAME, 'item-detail__section-title').text.split(
                                              ')')[0].split('/')[0].split(':')[1]

                    try:
                        more_choices = driver.find_element(By.CLASS_NAME, 'buying-choices-contents')
                        other_listings = more_choices.find_elements(By.CLASS_NAME, 'buying-choices-contents__list')
                        for o in other_listings:
                            sub_figure = {
                                'jan_code': figure['jan_code'],
                                'store_id ': 1,
                                'currency_code': figure['currency_code'],
                                'price': 0,
                                'is_available': 1,
                                'is_limited_edition': figure['is_limited_edition'],
                                'condition': None,
                                'url': figure['url']
                            }

                            other_listing = o.find_element(By.CLASS_NAME,
                                                           'buying-choices-contents__list_price').text.split('\n')
                            sub_figure['price'] = float(other_listing[0].replace(',', '').replace('JPY', ''))
                            sub_figure['condition'] = other_listing[1].replace('Condition', '').split('Box')[0].strip()
                            used_df = pd.concat([used_df, pd.DataFrame([sub_figure])], ignore_index=True)

                    except:
                        None

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(0.5)

                    used_df = pd.concat([used_df, pd.DataFrame([figure])], ignore_index=True)

            #####
            else:
                print('figure not previously in table, adding to table')
                used_df = pd.DataFrame()

                availability_check = f.find_element(By.CLASS_NAME, 'newly-added-items__item__tag-list__item')
                if 'Order Closed' in availability_check.text:
                    figure['is_available'] = 0

                limited_check = f.find_element(By.CLASS_NAME,
                                               'newly-added-items__item__tag-list__line.newly-added-items__item__tag-list__line_limited')
                if 'Limited' in limited_check.text:
                    figure['is_limited_edition'] = 1

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

                figure['condition'] = 'Item:' + \
                                      driver.find_element(By.CLASS_NAME, 'item-detail__section-title').text.split(')')[
                                          0].split('/')[0].split(':')[1]

                try:
                    more_choices = driver.find_element(By.CLASS_NAME, 'buying-choices-contents')
                    other_listings = more_choices.find_elements(By.CLASS_NAME, 'buying-choices-contents__list')
                    for o in other_listings:
                        sub_figure = {
                            'jan_code': figure['jan_code'],
                            'store_id ': 1,
                            'currency_code': figure['currency_code'],
                            'price': 0,
                            'is_available': 1,
                            'is_limited_edition': figure['is_limited_edition'],
                            'condition': None,
                            'url': figure['url']
                        }

                        other_listing = o.find_element(By.CLASS_NAME, 'buying-choices-contents__list_price').text.split(
                            '\n')
                        sub_figure['price'] = float(other_listing[0].replace(',', '').replace('JPY', ''))
                        sub_figure['condition'] = other_listing[1].replace('Condition', '').split('Box')[0].strip()
                        used_df = pd.concat([used_df, pd.DataFrame([sub_figure])], ignore_index=True)

                except:
                    None

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(0.5)

                used_df = pd.concat([used_df, pd.DataFrame([figure])], ignore_index=True)

            params = urllib.parse.quote_plus(
                "DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-QLGCSG7;DATABASE=figure_tracker;Trusted_Connection=yes;Encrypt=no;")
            engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params))
            used_df.to_sql('PreownedListings', engine, if_exists='append', index=False)

        #####
        else:
            figure = {
                'jan_code': jan,
                'store_id ': 1,
                'currency_code': None,
                'price': 0,
                'is_preorder': 0,
                'is_available': 1,
                'is_limited_edition': 0,
                'url': None
            }

            if new_exists:
                print('figure exists in table. updating table')
                url_check = f.find_element(By.TAG_NAME, 'a')
                figure['url'] = url_check.get_attribute('href')

                availability_check = f.find_element(By.CLASS_NAME, 'newly-added-items__item__tag-list__item')
                if 'Order Closed' in availability_check.text:
                    figure['is_available'] = 0

                limited_check = f.find_element(By.CLASS_NAME,
                                               'newly-added-items__item__tag-list__line.newly-added-items__item__tag-list__line_limited')
                if 'Limited' in limited_check.text:

                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(0.5)
                    driver.get(figure['url'])
                    time.sleep(3)

                    jp_price = driver.find_element(By.CLASS_NAME, 'item-detail__price_selling-price')
                    figure['price'] = float(jp_price.text.replace('JPY', '').replace(',', ''))
                    about_all = driver.find_elements(By.CLASS_NAME, 'item-about__data')

                    conn = pyodbc.connect(
                        'Driver={SQL Server};' 'Server=DESKTOP-QLGCSG7;' 'Database=figure_tracker;' 'Trusted_Connection=yes;')
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE NewListings SET price = {} WHERE jan_code = '{}' AND is_limited_edition = 1".format(
                            figure['price'], figure['jan_code']))
                    cursor.execute(
                        "UPDATE NewListings SET is_available = {} WHERE jan_code = '{}' AND is_limited_edition = 1".format(
                            figure['is_available'], figure['jan_code']))

                    cursor.commit()
                    cursor.close()

                else:
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

                    conn = pyodbc.connect(
                        'Driver={SQL Server};' 'Server=DESKTOP-QLGCSG7;' 'Database=figure_tracker;' 'Trusted_Connection=yes;')
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE NewListings SET price = {} WHERE jan_code = '{}' AND is_limited_edition = 1".format(
                            figure['price'], figure['jan_code']))
                    cursor.execute(
                        "UPDATE NewListings SET is_available = {} WHERE jan_code = '{}' AND is_limited_edition = 0".format(
                            figure['is_available'], figure['jan_code']))

                    cursor.commit()
                    cursor.close()

            ######
            else:
                print('figure not previously in table, adding to table')
                new_df = pd.DataFrame()

                availability_check = f.find_element(By.CLASS_NAME, 'newly-added-items__item__tag-list__item')
                if 'Order Closed' in availability_check.text:
                    figure['is_available'] = 0

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

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(0.5)

                new_df = pd.concat([new_df, pd.DataFrame([figure])], ignore_index=True)

                params = urllib.parse.quote_plus(
                    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-QLGCSG7;DATABASE=figure_tracker;Trusted_Connection=yes;Encrypt=no;")
                engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params))
                new_df.to_sql('NewListings', engine, if_exists='append', index=False)

    driver.close()


amiami_lookup('4560228206913')

def parse_new_page(driver, df):
    matching_params = driver.find_element(By.CLASS_NAME, 'new-items__inner')
    figure_general_box = matching_params.find_elements(By.CLASS_NAME, 'newly-added-items__item.nomore')
    for f in figure_general_box:

        figure_name = f.find_element(By.CLASS_NAME, 'newly-added-items__item__name')
        if 'Game-prize' in figure_name.text:
            continue

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

        if len(figure['jan_code']) < 1:
            continue

        df = pd.concat([df, pd.DataFrame([figure])], ignore_index=True)
    return df


def new_listing_table():

    driver = webdriver.Chrome()
    driver.get(
        "https://www.amiami.com/eng/search/list/?s_st_list_preorder_available=1&s_cate2=459&s_st_list_newitem_available=1")
    time.sleep(2)
    assert "AmiAmi" in driver.title
    time.sleep(2)

    new_figure_df = pd.DataFrame()

    new_figure_df = parse_new_page(driver, new_figure_df)
    time.sleep(3)
    for i in range(4):
        nextPage = driver.find_element(By.CLASS_NAME, 'pager__next')
        nextPage.click()
        time.sleep(3)
        new_figure_df = parse_new_page(driver, new_figure_df)

    print(tabulate(new_figure_df, headers = 'keys', tablefmt = 'psql'))
    driver.close()

    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-QLGCSG7;DATABASE=figure_tracker;Trusted_Connection=yes;Encrypt=no;")
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params))
    new_figure_df.to_sql('NewListings', engine, if_exists='append', index=False)

new_listing_table()


def parse_used_page(driver, df):
    matching_params = driver.find_element(By.CLASS_NAME, 'new-items__inner')
    figure_general_box = matching_params.find_elements(By.CLASS_NAME, 'newly-added-items__item.nomore')
    for f in figure_general_box:

        figure_name = f.find_element(By.CLASS_NAME, 'newly-added-items__item__name')
        if 'Game-prize' in figure_name.text:
            continue

        figure = {
            'jan_code': None,
            'store_id ': 1,
            'currency_code': None,
            'price': 0,
            'is_available': 1,
            'is_limited_edition': 0,
            'condition': None,
            'url': None
        }

        limited_check = f.find_element(By.CLASS_NAME,
                                       'newly-added-items__item__tag-list__line.newly-added-items__item__tag-list__line_limited')
        if 'Limited' in limited_check.text:
            figure['is_limited_edition'] = 1

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

        figure['condition'] = 'Item:' + \
                              driver.find_element(By.CLASS_NAME, 'item-detail__section-title').text.split(')')[0].split(
                                  '/')[0].split(':')[1]

        for a in about_all:
            if 'JAN code' in a.text:
                figure['jan_code'] = a.text.split('JAN code')[1].strip()

        try:
            more_choices = driver.find_element(By.CLASS_NAME, 'buying-choices-contents')
            other_listings = more_choices.find_elements(By.CLASS_NAME, 'buying-choices-contents__list')
            for o in other_listings:
                sub_figure = {
                    'jan_code': figure['jan_code'],
                    'store_id ': 1,
                    'currency_code': figure['currency_code'],
                    'price': 0,
                    'is_available': 1,
                    'is_limited_edition': figure['is_limited_edition'],
                    'condition': None,
                    'url': figure['url']
                }

                other_listing = o.find_element(By.CLASS_NAME, 'buying-choices-contents__list_price').text.split('\n')
                sub_figure['price'] = float(other_listing[0].replace(',', '').replace('JPY', ''))
                sub_figure['condition'] = other_listing[1].replace('Condition', '').split('Box')[0].strip()
                if len(figure['jan_code']) > 1:
                    df = pd.concat([df, pd.DataFrame([sub_figure])], ignore_index=True)
        except:
            None

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.5)

        if len(figure['jan_code']) < 1:
            continue

        df = pd.concat([df, pd.DataFrame([figure])], ignore_index=True)
    return df


def used_listing_table():
    usedListingDF = pd.DataFrame()

    driver = webdriver.Chrome()
    driver.get(
        "https://www.amiami.com/eng/search/list/?s_condition_flg=1&s_st_condition_flg=1&s_sortkey=preowned&s_cate2=459")
    time.sleep(2)
    assert "AmiAmi" in driver.title
    time.sleep(2)

    used_figure_df = pd.DataFrame()

    used_figure_df = parse_used_page(driver, used_figure_df)
    time.sleep(3)
    for i in range(4):
        nextPage = driver.find_element(By.CLASS_NAME, 'pager__next')
        nextPage.click()
        time.sleep(3)
        used_figure_df = parse_used_page(driver, used_figure_df)

    print(tabulate(used_figure_df, headers = 'keys', tablefmt = 'psql'))
    driver.close()

    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-QLGCSG7;DATABASE=figure_tracker;Trusted_Connection=yes;Encrypt=no;")
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params))
    used_figure_df.to_sql('PreownedListings', engine, if_exists='append', index=False)


#used_listing_table()



