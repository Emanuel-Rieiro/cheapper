import time
from random import randint
from scraper_tata import TataScraper
from scraper_devoto import DevotoScraper
from scraper_disco import DiscoScraper
from scraper_tienda import TiendaScraper
from scraper_eldorado import DoradoScraper

class ScraperOrchestrator():

    def __init__(self, driver, link, df):
        
        self.driver = driver 
        self.link = link
        self.df = df

        self.ecomm_name = link.split('.')[1]

        if self.ecomm_name == 'tata': self._tata_scraper_process()
        elif self.ecomm_name == 'disco': self._disco_scraper_process()
        elif self.ecomm_name == 'devoto': self._devoto_scraper_process()
        elif self.ecomm_name == 'tiendainglesa': self._tiendainglesa_scraper_process()
        elif self.ecomm_name == 'eldorado': self._eldorado_scraper_process()

    def _tata_scraper_process(self):
        
        self.scraper = TataScraper(self.driver, self.link, self.ecomm_name, self.df)
        
        self.scraper.go_to_website()

        self.scraper.close_popup_store()

        time.sleep(randint(3, 6))

        self.scraper.close_popup_coupon()

        time.sleep(randint(3, 6))

        self.scraper.close_popup_decreto()

        while not self.scraper.last_page:
            
            time.sleep(randint(3, 6))
            self.scraper.get_item_data()
            self.scraper.goto_next_page()

    def _disco_scraper_process(self):
        
        self.scraper = DiscoScraper(self.driver, self.link, self.ecomm_name, self.df)

        self.scraper.go_to_website()

        time.sleep(randint(3, 6))
        
        self.scraper.close_popup_store()

        while not self.scraper.last_page:
            
            time.sleep(randint(3, 6))
            self.scraper.get_item_data()
            self.scraper.goto_next_page()

    def _devoto_scraper_process(self):
        
        self.scraper = DevotoScraper(self.driver, self.link, self.ecomm_name, self.df)

        self.scraper.go_to_website()

        self.scraper.close_popup_store()

        while not self.scraper.last_page:
            
            time.sleep(randint(3, 6))
            self.scraper.get_item_data()
            self.scraper.goto_next_page()

    def _tiendainglesa_scraper_process(self):
        
        self.scraper = TiendaScraper(self.driver, self.link, self.ecomm_name, self.df)

        self.scraper.go_to_website()

        time.sleep(randint(3, 6))

        self.scraper.close_popup_store()

        while not self.scraper.last_page:
            
            time.sleep(randint(3, 6))
            self.scraper.get_item_data()
            self.scraper.goto_next_page()

    def _eldorado_scraper_process(self):
        
        self.scraper = DoradoScraper(self.driver, self.link, self.ecomm_name, self.df)
            