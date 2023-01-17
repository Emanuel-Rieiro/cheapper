import time
from random import randint
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class ClonScraper():

    def __init__(self, driver, link, ecomm_name, date, df):
        
        self.driver = driver
        self.df = df
        self.link = link
        self.last_page = False
        self.ecomm_name = ecomm_name
        self.date = date
        
    def go_to_website(self):

        print(f'go_to_website: {self.link}')
        self.driver.get(self.link) # go to link
        self.driver.implicitly_wait(randint(5, 10)) # wait a random of up to 10 seconds

    def scroll_bottom(self):

        paginador = self.driver.find_element(By.ID, "catalogoPaginado")

        while not self.last_page:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            tot = paginador.find_element(By.CLASS_NAME, 'tot').get_attribute('textContent')
            totAbs = paginador.find_element(By.CLASS_NAME, 'totAbs').get_attribute('textContent')

            if tot == totAbs:
                print('ultima pagina')
                self.last_page = True

            time.sleep(3)

    def get_item_data(self):

        print('get_item_data')
        items_wrapper = self.driver.find_element(By.ID, 'catalogoProductos')
        divs = items_wrapper.find_elements(By.CLASS_NAME, 'it')

        for div in divs:
        
            name = div.find_element(By.CLASS_NAME, 'tit').get_attribute('textContent')

            src = div.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')

            prices = []

            price_container = div.find_element(By.CLASS_NAME, 'precios')

            # price 1
            prices.append(price_container.find_element(By.CLASS_NAME, 'precio.venta').find_element(By.CLASS_NAME, 'monto').get_attribute("textContent"))
            
            # price 2
            price_tags = len(price_container.find_elements(By.CLASS_NAME, 'precio.venta'))
            if price_tags >= 2:
                try:
                    prices.append(price_container.find_element(By.CLASS_NAME, 'precio.lista').find_element(By.CLASS_NAME, 'monto').get_attribute("textContent"))
                except NoSuchElementException:
                    prices.append('')
            else:
                prices.append('')
        
            self.df.loc[len(self.df.index)] = [self.date, self.ecomm_name,name,src,prices[0],prices[1]]