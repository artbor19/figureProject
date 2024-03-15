import datetime
import itertools
import time

import sqlalchemy as db
from sqlalchemy import create_engine, URL
import urllib

from selenium import webdriver
from selenium.webdriver.common.by import By

from DTO.MFCConnectionURI import MFCConnectionURI
from DTO.SqlConnectionString import SqlConnectionString
from Items import get_links
import Items

driver = webdriver.Chrome()

uri = MFCConnectionURI(categoryId="1", page="1")
print(uri.get_connection_url())
links = Items.get_links(mfc_uri=uri, page=1, driver=driver)
figures = Items.get_item_detail_from_list(links=links, driver=driver)
print(len(figures), figures)
print(Items.get_item_detail(link="https://myfigurecollection.net/item/1411086", driver=driver))
print(len(links))
print(figures[0].releases[0].releaseJanCode)

# connectionString = SqlConnectionString()
#
# url_object = connectionString.get_sql_alchemy_mssql_connection_string()
# print(url_object)
#
# engine = db.create_engine(url_object)
# connection = engine.connect()
# metadata = db.MetaData()
# table = db.Table("Figures", metadata, autoload_with=engine)
# print(repr(metadata.tables['Figures']))
# print(table.columns.keys())
# query = table.select()
# insertQuery = table.insert().values(jan_code=figures[0].releases[0].releaseJanCode, name=figures[0].title,
#                                     manufacturer=figures[0].company, url="", create_date=time.strftime('%Y-%m-%d %H:%M:%S'),
#                                     update_date=time.strftime('%Y-%m-%d %H:%M:%S'))
# print(insertQuery)
# complied = insertQuery.compile()
# print(complied.params)
#
# result = connection.execute(insertQuery)
# connection.commit()
#
# connection.close()
