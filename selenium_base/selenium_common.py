import os
import time
from loguru import logger
from threading import Thread
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config_files.fund_param import MAX_WINDOW_NUM
from selenium.webdriver.chrome.options import Options

class SeleniumThread(Thread):
    def __init__(self, func, args=()):
        super().__init__()
        self.func = func
        self.args = args
        
    def run(self):
        try:
            self.result = self.func(*self.args)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
        
    def get_result(self):
        Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None

class SeleniumBase:
    def __init__(self, url, log_name, headless=True):
        self.url = url
        self.page_source = None
        self.log_storage_location = os.path.join(os.getcwd(), 'data')
        if headless:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            self.browser = webdriver.Chrome(chrome_options=chrome_options)
        else:
            self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.logger = self.get_logger(log_name)
        self.original_window_handler = self.browser.current_window_handle
        self.window_num = len(self.browser.window_handles)
        self.current_window_handler = self.browser.current_window_handle
        self.thread_list = []
        self.etree_content = None

    def download_web_page(self):
        self.page_source = self.browser.execute_script("return document.documentElement.outerHTML;")
        
    def get_logger(self, log_name):
        file_location = os.path.join(self.log_storage_location, log_name)
        logger.add(sink= file_location,
                    rotation='1 day',
                    enqueue=True,
                    backtrace=True,
                    diagnose=True,
                    level='INFO'    
                    )
        logger.info('store log at {}'.format(file_location))
        return logger

    def make_sure_web_ready(self, locator):
        self.logger.info('checking {}'.format(locator))
        self.wait.until(EC.presence_of_element_located(locator))

    def get_page_source(self, page_content=None):
        self.download_web_page()
        if not page_content:
            self.etree_content = etree.HTML(self.page_source)
        else:
            page_content = etree.HTML(self.page_source)
            return page_content