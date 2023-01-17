from random import randint
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains

class DevotoScraper():

    def __init__(self, driver, link, ecomm_name, df):
        
        self.driver = driver
        self.df = df
        self.link = link
        self.last_page = False
        self.ecomm_name = ecomm_name
        
    def go_to_website(self):

        print('go_to_website')
        self.driver.get(self.link) # go to link
        self.driver.implicitly_wait(randint(5, 10)) # implicitly wait a random of up to 10 seconds

    def close_popup_store(self):

        print('close_popup_store')

        try:
            self.driver.find_element(By.ID, 'btnConfirmaSucursal').click()

        except NoSuchElementException:
            print('Store element does not exist')
        except ElementNotInteractableException:
            print('Store element not interactable')

    def close_popup_suscription(self):

        try:
            self.driver.find_element(By.CLASS_NAME, 'wcqhv9e').click()

        except NoSuchElementException:
            print('Pop-up suscription element does not exist')
        except ElementNotInteractableException:
            print('Pop-up suscription element not interactable')


    def get_item_data(self):

        print('get_item_data')
        items_wrapper = self.driver.find_element(By.CLASS_NAME, 'vitrine.resultItemsWrapper')
        divs = items_wrapper.find_elements(By.CLASS_NAME, 'Product')

        for div in divs:

            name = div.find_element(By.CLASS_NAME, 'Product-title')
            name = name.find_element(By.CSS_SELECTOR, 'a').text

            src = div.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')

            prices = []
            prices_wrapper = div.find_element(By.CLASS_NAME, "Product-prices")

            # price 1
            p = prices_wrapper.find_element(By.CLASS_NAME, "Product-price")
            prices.append(p.find_element(By.CSS_SELECTOR,'span').get_attribute("textContent"))

            # price 2
            p = prices_wrapper.find_element(By.CLASS_NAME, "precio-antes")
            # try:
            #     prices.append(p.find_element(By.CSS_SELECTOR,'span').get_attribute("textContent"))
            # except NoSuchElementException:
            prices.append('')

            self.df.loc[len(self.df.index)] = [self.ecomm_name, name,src,prices[0],prices[1]]
    
    def goto_next_page(self):

        print('goto_next_page')
        pager_container = self.driver.find_element(By.CLASS_NAME, 'pager.bottom')

        footer = self.driver.find_element(By.CLASS_NAME, 'contenedor-apps')

        actions = ActionChains(self.driver)
        actions.move_to_element(footer).perform()

        try:
            pager_container.find_element(By.CLASS_NAME,'next').click()
        except ElementNotInteractableException:
            self.last_page = True
            print('ultima pagina')
