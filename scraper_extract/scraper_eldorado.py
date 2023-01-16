from random import randint
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

class DoradoScraper():

    def __init__(self, driver, link, ecomm_name, df):
        
        self.driver = driver
        self.df = df
        self.link = link
        self.last_page = False
        self.ecomm_name = ecomm_name
        
    def go_to_website(self):

        print('go_to_website')
        self.driver.get(self.link) # go to link
        self.driver.implicitly_wait(randint(5, 10)) # wait a random of up to 10 seconds

    def close_popup_store(self):

        print('close_popup_store')

        try:
            popup_store = self.driver.find_element("xpath", '//*[@role="dialog"]') # Get my store element
            popup_store_selector = popup_store.find_element(By.ID, 'store') 
            popup_store_selector.click() # Click to see stores
            popup_store_selector.find_element(By.ID, 'react-select-3-option-0').click() # click on first store
            popup_store.find_element(By.CSS_SELECTOR, 'button').click()

        except NoSuchElementException:
            print('Store element does not exist')

    def close_popup_coupon(self):

        try:
            popup_cupon = self.driver.find_element(By.ID, 'braindw_register') # find the element
            popup_cupon_close = popup_cupon.find_element(By.CLASS_NAME, "braindw_closepop") # get the close element
            popup_cupon_close.click() # close the pop-up

        except NoSuchElementException:
            print('Popup coupon element does not exist')

    def close_popup_suscription(self):

        try:
            popup_suscription = self.driver.find_element(By.ID, 'normal-slidedown') # find the element
            popup_suscription.find_element(By.ID, 'onesignal-slidedown-cancel-button').click() # click on cancel

        except NoSuchElementException:
            print('Popup suscription element does not exist')

    def close_popup_decreto(self):

        try:
            self.driver.find_element(By.CLASS_NAME, 'ub-emb-close').click()

        except NoSuchElementException:
            print('Element does not exist')

    def get_item_data(self):
        
        print('get_item_data')
        items_wrapper = self.driver.find_element(By.CLASS_NAME, 'styles__Container-tyimju-1')
        divs = items_wrapper.find_elements(By.CSS_SELECTOR, 'div')

        for div in divs:
        
            if div.get_attribute('data-sku'):

                name = div.find_element(By.CSS_SELECTOR, 'h2').text
                src = div.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')

                prices = []
                prices_wrapper = div.find_element(By.CLASS_NAME, "styles__Prices-msqlmx-11")
                prices_wrapper = prices_wrapper.find_elements(By.CSS_SELECTOR, 'p')

                for i in range(2):
                    try:
                        prices.append(prices_wrapper[i].text)
                    except IndexError:
                        prices.append('')

                self.df.loc[len(self.df.index)] = [self.ecomm_name, name,src,prices[0],prices[1]]
    
    def goto_next_page(self):

        print('goto_next_page')
        pager_container = self.driver.find_element(By.CLASS_NAME, 'styles__Container-sc-13trvf6-2')

        actions = ActionChains(self.driver)
        actions.move_to_element(pager_container).perform()

        buttons = pager_container.find_elements(By.CSS_SELECTOR, 'button')

        clickeado = False

        try:
            for button in buttons:
                spans = button.find_elements(By.CSS_SELECTOR,'span')
                for span in spans:
                    if span.text == 'siguiente':
                            button.click()
                            clickeado = True
                            break                
                if clickeado:
                    break

        except ElementClickInterceptedException:
            self.last_page = True
            print('ultima pagina')
