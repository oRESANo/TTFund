import sys, os
import time
from threading import Thread
from loguru import logger
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
sys.path.append(os.getcwd())
from config_files.fund_param import FUND_SEARCH_URL, MAX_THREAD_NUM, MAX_WINDOW_NUM
from selenium.webdriver.support import expected_conditions as EC
from selenium_base.selenium_common import SeleniumBase, SeleniumThread
from tt_web.fund import Fund

class CrackEastMoney(SeleniumBase):
    def __init__(self, url, log_name):
        super().__init__(url, log_name)
        self.locator = ()
        self.fund_list = []

    # grab all funding list
    def collapse_fund_list(self, locator):
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
    
    def get_fund_list(self, locator):
        self.collapse_fund_list(locator)
        self.get_page_source()
        _code = self.etree_content.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a[not(@title)]/text()')
        _link = self.etree_content.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a[not(@title)]/@href')
        _name = self.etree_content.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a/@title')
        # self.logger.info(_code)
        # self.logger.info(_link)
        # self.logger.info(_name)
        if len(_code) == len(_link) and len(_link) == len(_name):
            for i in range(len(_code)):
                self.fund_list.append(Fund(_code[i], _link[i], _name[i]))

    def parellel_process_start(self, locators):
        fund_index = 0
        while True:
            self.push_into_thread_list(self.fund_list[fund_index], locators)
            self.logger.info('add thread {}'.format(len(self.thread_list)))
            if len(self.thread_list) == MAX_THREAD_NUM or fund_index == len(self.fund_list)-1:
                self.process_thread_list()
            if fund_index >= len(self.fund_list):
                break
            else:
                fund_index = fund_index + 1

    def push_into_thread_list(self, fund, locators):
        thr = SeleniumThread(self.open_grab_close_tab, (fund,locators,))
        self.thread_list.append(thr)

    # parellel processing thread
    def process_thread_list(self):
        del_thr_list = []
        for thr in self.thread_list: # ONLY have 5 threads at most
            thr.start()
            ret = thr.get_result()
            self.logger.info(self.thread_list)
            if ret:
                self.logger.info(ret)
                del_thr_list.append(thr)
            else:
                self.logger.error('reach max window number')
            self.logger.info(del_thr_list)
        for del_thr in del_thr_list:
            self.logger.info('delete ', del_thr)
            self.thread_list.remove(del_thr)
            self.logger.info('thread list length: {}'.format(len(self.thread_list)))
        for i in range(len(self.browser.window_handles)):
            self.browser.switch_to_window(self.browser.window_handles[i])
            self.browser.close()
            self.logger.info('close {}'.format(self.browser.window_handles[i]))

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
        fund.get_fund_quartile_ranke(self.etree_content.xpath('//li[@id="increaseAmount_stage"]//td/h3/text()'))
        fund.get_fund_rank_score()
        fund.holding_stock_list['stock_name'] = self.etree_content.xpath('//li[@class="position_shares"]//td[@class="alignLeft"]/a/text()')
        tmp = []
        _percentage_list = self.etree_content.xpath('//li[@class="position_shares"]/div[@class="poptableWrap"]//td[@class="alignRight bold"]/text()')
        print(_percentage_list)
        for _percentage in _percentage_list:
            tmp.append(float(_percentage[:-1])/100)
        fund.holding_stock_list['holding_percentage'] = tmp
        fund.net_worth_link = self.etree_content.xpath('//li[@id="position_shares"]//div[@class="poptableWrap_footer"]//a/@href')


    # Entrance for grab all fund data
    def get_fund_data(self, fund_locator):
        self.parellel_process_start(fund_locator)

    def run(self, fund_list_locator, fund_locator):
        self.get_fund_list(fund_list_locator)
        self.get_fund_data(fund_locator)
                    

if __name__ == '__main__':
    a = CrackEastMoney(FUND_SEARCH_URL.format(key='消费'), 'EastMoney.log')
    a.run((By.CLASS_NAME, "search-result"), [(By.ID, "IncreaseAmount"), (By.ID, "quotationItem_DataTable"), (By.CLASS_NAME, "titleItems tabBtn titleItemActive")])