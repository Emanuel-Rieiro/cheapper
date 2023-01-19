import datetime
import pandas as pd
from selenium import webdriver
from scraper_extract.scraper_orchestator import ScraperOrchestrator

def main():

    # Starting the driver in full-screen
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window() 

    # Dataframe for data
    df = pd.DataFrame(columns = ['date','ecomm_name','name','src','price_1','price_2'])

    # Get links of pages we are scraping
    with open('scraper_extract/links.txt', 'r') as links_txt: links = links_txt.readlines()

    # Date
    date = datetime.datetime.today().strftime('%d-%m-%Y')

    # Loop trough the links, updating our dataset
    for link in links:
        try:
            web_scraper = ScraperOrchestrator(driver, link, date, df)
            df = web_scraper.df
        except:
            print('Error en:', link)

    path = f'tmp/webscraping_results_{date}.csv'

    df.to_csv(path, index = False)

    return path

if __name__ == '__main__':

    file = main()

    print(f'{file} succesfully created')