import time
from random import randint
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class DoradoScraper():

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

    def get_item_data(self):
        
        print('get_item_data')
        articles = self.driver.find_elements(By.CSS_SELECTOR, 'article')

        for article in articles:

            try:

                name = article.find_element(By.CSS_SELECTOR, 'h3')
                name = name.find_element(By.CSS_SELECTOR, 'span').get_attribute("textContent")

                src = article.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')

                prices = []

                price_container = article.find_element(By.CLASS_NAME, 'eldoradouy-product-price-custom-currency-0-x-sellingPriceInLocalCurrency')

                # price 1
                prices.append(price_container.find_elements(By.CSS_SELECTOR, 'span')[1].get_attribute("textContent"))

                # price 2
                prices.append('')

                self.df.loc[len(self.df.index)] = [self.date, self.ecomm_name,name,src,prices[0],prices[1]]
        
            except:
                pass
    
    def scroll_bottom(self):

        while not self.last_page:

            time.sleep(randint(5, 10))

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            try:
                class_name = 'vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h-small t-action--small bg-action-primary b--action-primary c-on-action-primary hover-bg-action-primary hover-b--action-primary hover-c-on-action-primary pointer'
                self.driver.find_element(By.CLASS_NAME, class_name.replace(' ','.')).click()
            except NoSuchElementException:
                self.last_page = True
                print('ultima pagina')