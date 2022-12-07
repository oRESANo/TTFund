import os
import time
from loguru import logger
from selenium import webdriver
from web_common.web_base import WebPage
from selenium.webdriver.support.wait import WebDriverWait
from config_files.fund_param import MAX_WINDOW_NUM

class SeleniumBase:
    def __init__(self, url, log_name):
        self.url = url
        self.page_source = None
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.browser.get(self.url)
        self.logger = self.get_logger(log_name)
        self.original_window_handler = self.browser.current_window_handle
        self.window_num = len(self.browser.window_handles)
        self.current_window_handler = self.browser.current_window_handle
        
    def grab_web_page(self):
        self.page_source = self.browser.execute_script("return document.documentElement.outerHTML;")
        
    def get_logger(self, log_name):
        _file_location = os.path.join(os.getcwd(),'data/'+log_name)
        logger.add(sink=_file_location,
                    rotation='1 day',
                    enqueue=True,
                    backtrace=True,
                    diagnose=True,
                    level='INFO'    
                    )
        logger.info('store log at {}'.format(_file_location))
        return logger
    
    # open different tab in browser
    def open_tab(self, fund):
        if self.window_num <= MAX_WINDOW_NUM:
            self.browser.switch_to.new_window('tab')
            self.window_num = len(self.browser.window_handles)
            self.current_window_handler = self.browser.current_window_handle
            self.browser.get(fund.url)
            self.logger.info('open {}'.format(fund.url))
            time.sleep(2)
            return True
        else:
            return False
        