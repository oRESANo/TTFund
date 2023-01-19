import sys, os
import time
import click
from threading import Thread
from loguru import logger
from lxml import etree
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
sys.path.append(os.getcwd())
from config_files.fund_param import FUND_SEARCH_URL, MAX_THREAD_NUM, MAX_WINDOW_NUM, fund_list_locators, fund_locators, fund_networth_locators
from selenium.webdriver.support import expected_conditions as EC
from selenium_base.selenium_common import SeleniumBase, SeleniumThread
from tt_web.fund_sup.fund_common import clean_fund_networth_data, order_fund_by_score
from tt_web.fund import Fund

class CrackEastMoney(SeleniumBase):
    def __init__(self, search_key_word, log_name, headless, specific_fund=None):
        url = FUND_SEARCH_URL.format(key=search_key_word)
        super().__init__(url, log_name, headless)
        self.search_key_word = search_key_word
        self.specific_fund = specific_fund
        self.locator = ()
        self.fund_list = []
        self.fund_networth_data_storage_location = os.path.join(os.getcwd(), 'data/net_worth/{}'.format(self.search_key_word))
        try:
            os.mkdir(self.fund_networth_data_storage_location)
        except FileExistsError as e:
            self.logger.info('{} exists'.format(self.fund_networth_data_storage_location))
        self.code_list = [] # self.etree_content fund code list
        self.link_list = [] # self.etree_content fund link list
        self.name_list = [] # self.etree_content fund name list

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
        self.get_fund_list_details()
        if len(self.code_list) == len(self.link_list) and len(self.link_list) == len(self.name_list):
            if self.specific_fund:
                self.single_fund_search()
                return
            for i in range(len(self.code_list)):
            # FOR TEST, ONLY crawl 5 funds
            # for i in range(5):
                self.name_list[i] = self.name_list[i].replace('/', '_')
                self.fund_list.append(Fund(self.code_list[i], self.link_list[i], self.name_list[i], self.logger))
        else:
            self.logger.error('fund self.code_list {code_len}, fund self.link_list {link_len} and fund self.name_list {name_len} length not equal, something wrong'.format(code_len=len(self.code_list), link_len=len(self.link_list), name_len=len(self.name_list)))

    def get_fund_list_details(self):
        self.code_list = self.etree_content.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a[not(@title)]/text()')
        self.link_list = self.etree_content.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a[not(@title)]/@href')
        self.name_list = self.etree_content.xpath('//*[@id="jj"]//tbody//td[not(@class)]//a/@title')

    def single_fund_search(self):
        for i in range(len(self.code_list)):
            if self.specific_fund == self.name_list[i]:
                self.name_list[i] = self.name_list[i].replace('/', '_')
                self.fund_list.append(Fund(self.code_list[i], self.link_list[i], self.name_list[i], self.logger))
                return

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
        # Re-order fund list by fund rank score
        self.fund_list = order_fund_by_score(self.fund_list)
        self.logger.warning('Top 5 fund '+str([fund.fund_name for fund in self.fund_list[0:5]]))

    def push_into_thread_list(self, fund, locators):
        thr = SeleniumThread(self.open_grab_close_tab, (fund,locators,))
        self.thread_list.append(thr)

    # parellel processing thread
    def process_thread_list(self):
        del_thr_list = []
        for thr in self.thread_list: # ONLY have 5 threads at most
            thr.start() # start open_grab_close_tab function
            ret = thr.get_result()
            if ret:
                self.logger.info('thread action successfully')
                del_thr_list.append(thr)
            else:
                self.logger.error('reach max window number')
        # start to delete thread
        for del_thr in del_thr_list:
            self.logger.info('delete {}'.format(del_thr))
            self.thread_list.remove(del_thr)
            self.logger.info('thread list length: {}'.format(len(self.thread_list)))
        # start to close tab, update window number
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
            fund.get_fund_details(self.etree_content)
            return True
        else:
            return False

    def fund_networth_flip_page(self):
        try:
            click_button = self.browser.find_element(By.XPATH, '//div[@class="pagebtns"]/label[text()="下一页"]')
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
        final_page = 0
        # get 5 best fund networth details
        for fund in self.fund_list[0:5]:
            self.browser.get(fund.net_worth_link)
            while True:
            # FOR TEST, only crawl first 5 pages
            # for _ in range(5):
                for locator in locators:
                    self.make_sure_web_ready(locator)
                self.get_page_source()
                current_page,final_page = fund.get_fund_networth_details(self.etree_content, final_page)
                self.logger.info('current_page {}'.format(current_page))
                self.logger.info('final_page {}'.format(final_page))
                self.fund_networth_flip_page()
                if current_page == final_page:
                    final_page = 0
                    break
            fund.net_worth = clean_fund_networth_data(fund.net_worth)
            fund.net_worth.to_excel(os.path.join(self.fund_networth_data_storage_location, fund.fund_name+'.xlsx'))
            self.logger.info('finish crawling {} networth'.format(fund.fund_name))

    def run(self, fund_list_locators, fund_locators, fund_networth_locators):
        self.get_fund_list(fund_list_locators)
        self.get_fund_data(fund_locators)
        self.get_fund_networth(fund_networth_locators)

@click.command()
@click.option('--key', required=True, type=str)
@click.option('--log', default='EastMoney.log', type=str)
@click.option('--headless', default=True, type=bool)
@click.option('--specific_fund', default=None, type=str)
def main(key, log, headless, specific_fund):
    if specific_fund:
        a = CrackEastMoney(key, log, headless, specific_fund)
        a.run(fund_list_locators,
            fund_locators,
            fund_networth_locators)
    else:
        key_words = key.split(',')
        for key_word in key_words:
            a = CrackEastMoney(key_word, log, headless)
            a.run(fund_list_locators,
                fund_locators,
                fund_networth_locators)

if __name__ == '__main__':
    main()