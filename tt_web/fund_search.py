import sys, os
import time
from threading import Thread
from loguru import logger
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
sys.path.append(os.getcwd())
from config_files.fund_param import FUND_SEARCH_URL, MAX_THREAD_NUM, MAX_WINDOW_NUM, fund_list_locators, fund_locators, fund_networth_locators
from selenium.webdriver.support import expected_conditions as EC
from selenium_base.selenium_common import SeleniumBase, SeleniumThread
from tt_web.fund import Fund

class CrackEastMoney(SeleniumBase):
    def __init__(self, url, log_name, headless=True):
        super().__init__(url, log_name, headless)
        self.locator = ()
        self.fund_list = []

    # grab all funding list
    def collapse_fund_list(self, locators):
        for locator in locators:
            self.make_sure_web_ready(locator)
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
    
    def get_fund_list(self, locators):
        self.browser.get(self.url)
        self.collapse_fund_list(locators)
        self.get_page_source()
        code = self.etree_content.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a[not(@title)]/text()')
        link = self.etree_content.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a[not(@title)]/@href')
        name = self.etree_content.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a/@title')
        if len(code) == len(link) and len(link) == len(name):
            for i in range(len(code)):
                self.fund_list.append(Fund(code[i], link[i], name[i]))

    def get_fund_data(self, locators):
        fund_index = 0
        while True:
            self.push_into_thread_list(self.fund_list[fund_index], locators)
            self.logger.info('add thread {}'.format(len(self.thread_list)))
            if len(self.thread_list) == MAX_THREAD_NUM or fund_index == len(self.fund_list)-1:
                # start thread
                self.process_thread_list()
            fund_index = fund_index + 1
            if fund_index >= len(self.fund_list):
                self.logger.info('reach end of thread list, break out')
                break

    def push_into_thread_list(self, fund, locators):
        thr = SeleniumThread(self.open_grab_close_tab, (fund,locators,))
        self.thread_list.append(thr)

    # parellel processing thread
    def process_thread_list(self):
        del_thr_list = []
        for thr in self.thread_list: # ONLY have 5 threads at most
            thr.start() # start open_grab_close_tab function
            ret = thr.get_result()
            # self.logger.info(self.thread_list)
            if ret:
                self.logger.info('thread action successfully')
                del_thr_list.append(thr)
            else:
                self.logger.error('reach max window number')
            # self.logger.info(del_thr_list)
        # start to delete thread
        for del_thr in del_thr_list:
            self.logger.info('delete {}'.format(del_thr))
            self.thread_list.remove(del_thr)
            self.logger.info('thread list length: {}'.format(len(self.thread_list)))
        # start to close tab
        # update window number
        while self.browser.window_handles[0] != self.browser.window_handles[-1]:
            self.logger.info('close {}'.format(self.browser.window_handles[-1]))
            self.browser.switch_to.window(self.browser.window_handles[-1])
            self.browser.close()
        self.window_num = len(self.browser.window_handles)
        self.logger.info('switch to origin window, current total window length: {}'.format(self.window_num))
        self.browser.switch_to.window(self.browser.window_handles[0])

    # open different tab in browser
    def open_grab_close_tab(self, fund, locators):
        if self.window_num <= MAX_WINDOW_NUM:
            self.browser.switch_to.new_window('tab')
            self.window_num = len(self.browser.window_handles)
            self.browser.get(fund.fund_url)
            self.logger.info('open {}'.format(fund.fund_url))
            for locator in locators:
                self.make_sure_web_ready(locator)
            self.get_page_source()
            # TODO grab fund details
            self.get_fund_details(fund)
            return True
        else:
            return False
        
    def get_fund_details(self, fund):
        self.logger.info('starting to crawl fund details {}'.format(\
                        fund.fund_name))
        fund.get_fund_quartile_rank(self.etree_content.xpath('//li[@id="increaseAmount_stage"]//td/h3/text()'))
        fund.get_fund_rank_score()
        fund.holding_stock_list['stock_name'] = self.etree_content.xpath('//li[@class="position_shares"]//td[@class="alignLeft"]/a/text()|//li[@class="position_shares"]//td[@class="alignLeft"]/div/text()')
        tmp = []
        percentage_list = self.etree_content.xpath('//li[@class="position_shares"]/div[@class="poptableWrap"]//td[@class="alignRight bold"]/text()')
        for percentage in percentage_list:
            if percentage[-1] == '%':
                tmp.append(float(percentage[:-1])/100)
            else:
                # dont append anything because stock list will be less
                self.logger.warning('holding_percentage is wrong')
        fund.holding_stock_list['holding_percentage'] = tmp
        # stock holding list
        self.logger.info(list(fund.holding_stock_list['stock_name']))
        self.logger.info(percentage_list)
        # stock net worth link
        fund.net_worth_link = self.etree_content.xpath('//li[@id="position_shares"]//div[@class="poptableWrap_footer"]//a/@href')

    # TODO edit XPATh element
    def fund_networth_flip_page(self):
        try:
            click_button = self.browser.find_element(By.XPATH, '//div[@class="pagebtns"]/label[8]')
            ActionChains(self.browser)\
                .move_to_element(click_button)\
                .pause(0.5)\
                .click(click_button)\
                .perform()
            time.sleep(0.5)
        except:
            pass

    # flip fund networth page
    def get_fund_networth(self, locators):
        for fund in self.fund_list:
            while 
            for locator in locators:
                self.make_sure_web_ready(locator)
            self.get_fund_networth_details(fund)
            self.fund_networth_flip_page()
    
    # TODO: need to refresh page source and keep crawling data
    def get_fund_networth_details(self, fund):
            self.logger.info('starting to crawl fund networth details {}'.format(\
                        fund.fund_name))
            fund.net_worth_web_page = self.get_page_source(fund.net_worth_web_page)
            fund.net_worth['date'].append(fund.net_worth_web_page.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[1]/text()'))
            fund.net_worth['unit_net_worth'].append(fund.net_worth_web_page.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[2]/text()'))
            fund.net_worth['accumulated_net_worth'].append(fund.net_worth_web_page.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[3]/text()'))
            fund.net_worth['daily_return'].append(fund.net_worth_web_page.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[4]/text()'))  

    def run(self, fund_list_locators, fund_locators, fund_networth_locators):
        self.get_fund_list(fund_list_locators)
        self.get_fund_data(fund_locators)
        self.get_fund_networth(fund_networth_locators)

if __name__ == '__main__':
    a = CrackEastMoney(FUND_SEARCH_URL.format(key='消费'), 'EastMoney.log')
    a.run(fund_list_locators, fund_locators, fund_networth_locators)