import urllib
import requests
import pandas as pd
from random import randint
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from scraper_orchestator import ScraperOrchestrator

if __name__ == '__main__':

    # Starting the driver in full-screen
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window() 

    # Dataframe for data
    df = pd.DataFrame(columns = ['ecomm_name','name','src','price_1','price_2'])

    # Get links of pages we are scraping
    with open('links.txt', 'r') as links_txt: links = links_txt.readlines()

    # Loop trough the links, updating our dataset
    for link in links:
        web_scraper = ScraperOrchestrator(driver, link, df)
        df = web_scraper.df

    df.to_csv('webscraping_results.csv')