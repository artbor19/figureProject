import itertools

import sqlalchemy as db
from sqlalchemy import create_engine, URL
import urllib

from selenium import webdriver
from selenium.webdriver.common.by import By

from DTO.MFCConnectionURI import MFCConnectionURI
from DTO.SqlConnectionString import SqlConnectionString, get_sql_alchemy_mssql_connection_string
from Items import get_links
import Items

uri = MFCConnectionURI(categoryId="1", page="1")
print(uri.get_connection_url())
links = Items.get_links(mfc_uri=uri, page=1)
print(Items.get_item_detail(links))
print(len(links))

# connectionString = SqlConnectionString()
#
# url_object = get_sql_alchemy_mssql_connection_string(connectionString.get_sql_connection_string())
# print(url_object)

# engine = db.create_engine(url_object)
# connection = engine.connect()
# metadata = db.MetaData()
# table = db.Table("Figures", metadata, autoload_with=engine)
# print(repr(metadata.tables['Figures']))
# print(table.columns.keys())
# query = table.select()
# print(query)
#
# connection.close()
