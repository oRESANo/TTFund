import sys, os
import time
from loguru import logger
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
sys.path.append(os.getcwd())
from config_files.fund_param import FUND_SEARCH_URL
from selenium.webdriver.support import expected_conditions as EC
from selenium_base.selenium_common import SeleniumBase
from tt_web.fund import Fund

class CrackEastMoney(SeleniumBase):
    def __init__(self, url, log_name):
        super().__init__(url, log_name)
        self.locator = ()
        self.fund_list = []

    # grab all funding list
    def collapse_fund_list(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        try:
            click_button = self.browser.find_element(By.XPATH, '//a[@data-more="jj"]')
            ActionChains(self.browser)\
                .move_to_element(click_button)\
                .pause(0.5)\
                .click(click_button)\
                .perform()
            time.sleep(2)
        except:
            pass
    
    def get_fund_list(self):
        e = etree.HTML(self.page_source)
        _code = e.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a[not(@title)]/text()')
        _link = e.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a[not(@title)]/@href')
        _name = e.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a/@title')
        self.logger.info(_code)
        self.logger.info(_link)
        self.logger.info(_name)
        if len(_code) == len(_link) and len(_link) == len(_name):
            for i in range(len(_code)):
                self.fund_list.append(Fund(_code[i], _link[i], _name[i]))
    
    def run(self, locator):
        self.collapse_fund_list(locator)
        self.grab_web_page()
        self.get_fund_list()
        # put fund_list obj into open tab method
        for _fund in self.fund_list:
            if self.open_tab(_fund):
                

if __name__ == '__main__':
    a = CrackEastMoney(FUND_SEARCH_URL.format(key='消费'), 'EastMoney.log')
    a.collapse_fund_list((By.CLASS_NAME, "search-result"))
    a.grab_web_page()
    a.get_fund_list()