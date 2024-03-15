import itertools
import locale

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from dateutil.parser import parse
import datetime
import re
from DTO.FigureDTO import FigureDTO
from DTO.ReleaseDTO import ReleaseDTO
from MyHTMLParser import MyHTMLParser
from DTO.MFCConnectionURI import MFCConnectionURI
from decimal import Decimal


def get_links(mfc_uri: MFCConnectionURI, page: int, driver: WebDriver, ):
    links = []
    for i in itertools.count(start=page):
        mfc_uri.set_page(i)
        search_url = mfc_uri.get_connection_url()

        driver.get(search_url)

        element = driver.find_elements(By.XPATH, ".//span[contains(@class, 'item-icon')]//a[@href]")
        links += [e.get_attribute("href") for e in element]

        # if len(element) == 0:
        break

    return links


def get_item_detail_from_list(links: list[str], driver: WebDriver):
    list_figures = []
    for link in links[:1]:
        list_figures.append(get_item_detail(link, driver))
    return list_figures


def get_item_detail(link: str, driver: WebDriver):
    driver.get(link)
    figure = FigureDTO()
    try:
        try:
            title = driver.find_element(By.XPATH,
                                        ".//div[contains(@class, 'content-headline')]//h1[contains(@class, 'title')]")
            figure.title = title.text
        except Exception as ex:
            figure.title = ""
            print("Title not available", ex.message if hasattr(ex, "message") else ex)

        try:
            origin = driver.find_element(By.XPATH, ".//div[text()='Origin']//following::span")
            figure.origin = origin.text
            # print(origin.text, origin.get_attribute("switch"))
        except Exception as ex:
            figure.origin = ""
            print("Origin not available", ex.message if hasattr(ex, "message") else ex)

        try:
            figure.character = []
            character = driver.find_element(By.XPATH, ".//div[contains(text(), 'Character')]//following::span")
            figure.character.append(character.text)
            # print(character.text, character.get_attribute("switch"))
        except Exception as ex:
            figure.character = []
            print("Character not available", ex.message if hasattr(ex, "message") else ex)

        try:
            figure.company = []
            company = driver.find_element(By.XPATH, ".//div[contains(text(), 'Compan')]//following::span")
            figure.company.append(company.text)
            # print(company.text, company.get_attribute("switch"))
        except Exception as ex:
            figure.company = []
            print("Company not available", ex.message if hasattr(ex, "message") else ex)

        try:
            releases = driver.find_elements(By.XPATH,
                                            ".//a[contains(@class, 'time')]//parent::div[contains(@class, 'data-value')]")
            figure.releases = []
            locale.setlocale(locale.LC_ALL, '')

            for release in releases:
                htmlParser = MyHTMLParser()
                htmlParser.feed(release.get_attribute('innerHTML'))
                release = ReleaseDTO()

                for d in htmlParser.data:
                    d = d.strip()
                    if not release.releaseDate:
                        try:
                            release.releaseDate = (parse(d, default=datetime.datetime(2000, 1, 1)))
                        except Exception as ex:
                            pass

                    if not release.releasePrice:
                        if re.fullmatch("[0-9]*[.,]*[0-9]*[.,]*[0-9]*[.,]+[0-9]*", d):
                            release.releasePrice = Decimal(locale.atof(d))
                    if not release.releaseCurrency:
                        if "jpy" in d.lower():
                            release.releaseCurrency = "jpy"
                        elif "cny" in d.lower():
                            release.releaseCurrency = "cny"
                        elif "usd" in d.lower():
                            release.releaseCurrency = "usd"
                    if not release.releaseJanCode:
                        if re.fullmatch("^45\\d+", d) or re.fullmatch("^49\\d+", d):
                            release.releaseJanCode = d

                figure.releases.append(release)
        except Exception as ex:
            figure.releases = []
            print("Releases not available", ex.message if hasattr(ex, "message") else ex)

        return figure

        time.sleep(1)
    except Exception as ex:
        print(link)
        print(ex)
    # pd.DataFrame()
    return 0
