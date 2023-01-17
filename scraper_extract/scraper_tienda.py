from random import randint
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

class TiendaScraper():

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

    def close_popup_store(self):

        print('close_popup_store')

        # sucursal
        try:
            self.driver.find_element(By.ID, 'MPW0078GRID1TABLE_0001').click()

        except NoSuchElementException:
            print('Store element does not exist')

    def get_item_data(self):

        print('get_item_data')
        items_wrapper = self.driver.find_element(By.ID, 'GridresultsContainerTbl')
        divs = items_wrapper.find_elements(By.CLASS_NAME, 'card-product-section')

        for div in divs:


            name = div.find_element(By.CLASS_NAME, 'card-product-name').get_attribute("textContent")

            src = div.find_element(By.CLASS_NAME, 'card-product-img').get_attribute('src').replace('small','large')

            prices = []

            # price 1
            prices.append(div.find_element(By.CLASS_NAME,'ProductPrice').get_attribute("textContent").replace('$',''))

            # price 2
            prices.append('')

            self.df.loc[len(self.df.index)] = [self.date, self.ecomm_name,name,src,prices[0],prices[1]]
    
    def goto_next_page(self):

        print('goto_next_page')
        pager_container = self.driver.find_element(By.ID, 'W0074SECTION1')

        actions = ActionChains(self.driver)
        actions.move_to_element(pager_container).perform()

        pager_buttons = pager_container.find_elements(By.CSS_SELECTOR,'a')

        next_page = False

        for button in pager_buttons:
            if button.get_attribute("textContent") == '>':
                button.click()
                next_page = True

        if next_page == False:
            self.last_page = True
            print('ultima pagina')
