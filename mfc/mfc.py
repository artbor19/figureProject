import itertools

import sqlalchemy as db
from sqlalchemy import create_engine, URL
import urllib

from selenium import webdriver
from selenium.webdriver.common.by import By

baseUrl = "https://myfigurecollection.net/?"
searchCriteria = {
    "tab": "calendar",
    "rootId": "0",
    "status": "-1",
    "categoryId": "-1",
    "domainId": "-1",
    "noReleaseDate": "0",
    "releaseTypeId": "0",
    "ratingId": "0",
    "isCastoff": "0",
    "hasBootleg": "0",
    "tagId": "0",
    "noBarcode": "0",
    "clubId": "0",
    "isDraft": "0",
    "year": "2024",
    "month": "1",
    "acc": "0",
    "separator": "0",
    "sort": "insert",
    "output": "2",
    "current": "categoryId",
    "order": "desc",
    "page": "1",
    "_tb": "item"
}

links = []

# for i in itertools.count(start=1):
#     searchCriteria["page"] = str(i)
#     searchUrl = baseUrl + '&'.join(f"{s}={searchCriteria[s]}" for s in searchCriteria)
#
#     driver = webdriver.Chrome()
#     driver.get(searchUrl)
#
#     element = driver.find_elements(By.XPATH, ".//span[contains(@class, 'item-icon')]//a[@href]")
#     links += [e.get_attribute("href") for e in element]
#
#     if len(element) == 0:
#         break
#
# print(len(links))

sqlConnectionParams = {
    "DRIVER": "{ODBC Driver 18 for SQL Server}",
    "SERVER": "localhost",
    "DATABASE": "figure_tracker",
    "Trusted_Connection": "yes",
    "Encrypt": "no"
}

connectionString = ';'.join(f"{s}={sqlConnectionParams[s]}" for s in sqlConnectionParams) + ';'

url_object = URL.create(drivername="mssql+pyodbc",
                        query={"odbc_connect": connectionString}
                        )
print(url_object)

engine = db.create_engine(url_object)
connection = engine.connect()
metadata = db.MetaData()
table = db.Table("Figures", metadata, autoload_with=engine)
print(repr(metadata.tables['Figures']))
print(table.columns.keys())
query = table.select()
print(query)

connection.close()
