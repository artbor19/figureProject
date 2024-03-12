import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from DTO.MFCConnectionURI import MFCConnectionURI
import time


def get_links(mfc_uri: MFCConnectionURI = MFCConnectionURI(), page: int = 1):
    links = []
    driver = webdriver.Chrome()
    for i in itertools.count(start=page):
        mfc_uri.set_page(i)
        search_url = mfc_uri.get_connection_url()

        driver.get(search_url)

        element = driver.find_elements(By.XPATH, ".//span[contains(@class, 'item-icon')]//a[@href]")
        links += [e.get_attribute("href") for e in element]

        # if len(element) == 0:
        break

    return links


def get_item_detail(links: list[str]):
    driver = webdriver.Chrome()
    li = []
    for link in links[:1]:
        driver.get(link)
        try:
            element = driver.find_element(By.XPATH,
                                          ".//div[contains(@class, 'content-headline')]//h1[contains(@class, 'title')]")
            print(element.text)
            origin = driver.find_element(By.XPATH, ".//div[text()='Origin']//following::span")
            print(origin.text, origin.get_attribute("switch"))
            character = driver.find_element(By.XPATH, ".//div[text()='Character']//following::span")
            print(character.text, character.get_attribute("switch"))
            company = driver.find_element(By.XPATH, ".//div[text()='Company']//following::span")
            print(company.text, company.get_attribute("switch"))
            releasesDate = driver.find_element(By.CLASS_NAME, "time")#driver.find_element(By.XPATH, ".//div[text()='Releases']//following::a")
            releasesPrice = driver.find_element(By.XPATH, ".//div[text()='Releases']//following::div")
            releasesJan = driver.find_element(By.XPATH, ".//a[contains(text(), '458')]")
            print(releasesDate.text)
            print(releasesPrice.text)
            print(releasesJan.get_attribute("content"), releasesJan.text)

            time.sleep(1)
        except Exception as ex:
            print(link)
            print(ex)
        # pd.DataFrame()
    return 0
