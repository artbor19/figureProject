from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://myfigurecollection.net/"
searchUrl = ("https://myfigurecollection.net/?"
             "tab=calendar&rootId=0&status=-1&categoryId=-1&domainId=-1&noReleaseDate=0&releaseTypeId=0"
             "&ratingId=0&isCastoff=0&hasBootleg=0&tagId=0&noBarcode=0&clubId=0&isDraft=0&year=2024&month=1"
             "&acc=0&separator=0&sort=insert&output=2&current=categoryId&order=desc&page=1&_tb=item")
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


driver = webdriver.Chrome()
driver.get(searchUrl)

element = driver.find_elements(By.XPATH, ".//span[contains(@class, 'item-icon')]//a[@href]")
links = [e.get_attribute("href") for e in element]
