import pandas as pd
import os, sys
import numpy as np
from collections import OrderedDict
sys.path.append(os.getcwd())
from config_files.fund_param import FUND_RANK_MULTI_PARAM, FUND_RANK_PERIOD, MAX_WINDOW_NUM, MAX_THREAD_NUM
from tt_web.fund_sup.fund_common import fund_rank_4_convert
from selenium_base.selenium_common import SeleniumBase, SeleniumThread

class Fund:
    def __init__(self, code, url, name, logger):
        self.fund_url = url
        self.fund_code = code
        self.fund_name = name
        self.holding_stock_list = pd.DataFrame(columns=['stock_name', 'holding_percentage'])
        self.net_worth_link = None
        self.net_worth_web_page = ' '
        self.net_worth = pd.DataFrame(columns=['date', 'unit_net_worth', 'accumulated_net_worth', 'daily_return'])
        # 优秀-4， 良好-3， 一般-1， 不佳-0 (0-25%, 25-50%, 50-75%, 75-100%) | @ 1 week, 1 month, 3months, 6months, from year begin, 1 year, 2 years, 3 years
        self.quartile_rank = [] # [4,2,1,4,0,1,3]
        self.rank_period = FUND_RANK_PERIOD # 1 week, 1 month, 3months, 6months, from year begin, 1 year, 2 years, 3 years
        self.rank_score_params = FUND_RANK_MULTI_PARAM # [0.05399097 0.24197072 0.35206533 0.39894228 0.35206533 0.24197072 0.05399097]
        self.rank_at_same_category = [] # [(rank, total_num)]
        self.top_10_holding_percetage = 0
        self.fund_rank_score = 0
        self.lack_data = False
        self.already_open_window = False # flag for selenium has already dealt with
        self.logger = logger
        
    # 获取fund的四分位排名, 数据不够重置flag
    def get_fund_quartile_rank(self, fund_rank_4_list:list):
        fund_rank_4_list.pop(4)
        for rank_4 in fund_rank_4_list:
            self.quartile_rank.append(fund_rank_4_convert(rank_4))
            if rank_4 == '--':
                self.lack_data = True

    def get_fund_rank_score(self):
        self.fund_rank_score = sum(self.quartile_rank * self.rank_score_params)

    def get_fund_details(self, etree_content):
        self.logger.info('starting to crawl self details {}'.format(\
                        self.fund_name))
        self.get_fund_quartile_rank(etree_content.xpath('//li[@id="increaseAmount_stage"]//td/h3/text()'))
        self.get_fund_rank_score()
        self.holding_stock_list['stock_name'] = etree_content.xpath('//li[@class="position_shares"]//td[@class="alignLeft"]/a/text()|//li[@class="position_shares"]//td[@class="alignLeft"]/div/text()')
        tmp = []
        percentage_list = etree_content.xpath('//li[@class="position_shares"]/div[@class="poptableWrap"]//td[@class="alignRight bold"]/text()')
        for percentage in percentage_list:
            if percentage[-1] == '%':
                tmp.append(float(percentage[:-1])/100)
            else:
                # dont append anything because stock list will be less
                self.logger.warning('holding_percentage is wrong')
        self.holding_stock_list['holding_percentage'] = tmp
        # stock holding list
        self.logger.info(list(self.holding_stock_list['stock_name']))
        self.logger.info(percentage_list)
        # stock net worth link
        self.net_worth_link = etree_content.xpath('//div[@id="Div2"]//div[@class="item_more"]/a/@href')[0]

    def get_fund_networth_details(self, etree_content, final_page):
        current_page = etree_content.xpath(
                        '//div[@class="pagebtns"]/label[@class="cur"]/text()')
        self.logger.info('starting to crawl fund networth details {} page {}'.format(\
                    self.fund_name, current_page))
        tmp_df = self.get_fund_networth_onepage_data(etree_content)
        self.net_worth = pd.concat([self.net_worth, tmp_df], ignore_index=True)
        if final_page == 0:
            final_page = etree_content.xpath(
                        '//div[@class="pagebtns"]/label[7]/text()')
        return current_page, final_page

    def get_fund_networth_onepage_data(self, etree_content):
        fund_date = pd.DataFrame(
                        etree_content.xpath(
                            '//table[@class="w782 comm lsjz"]/tbody/tr/td[1]/text()'),
                        columns=['date'])
        unit_worth = pd.DataFrame(
                        etree_content.xpath(
                            '//table[@class="w782 comm lsjz"]/tbody/tr/td[2]/text()'),
                        columns=['unit_net_worth'])
        accumulated_worth = pd.DataFrame(
                                etree_content.xpath(
                                    '//table[@class="w782 comm lsjz"]/tbody/tr/td[3]/text()'),
                                columns=['accumulated_net_worth'])
        daily_gain = pd.DataFrame(
                        etree_content.xpath(
                            '//table[@class="w782 comm lsjz"]/tbody/tr/td[4]/text()'),
                        columns=['daily_return'])
        tmp_df = fund_date.join(unit_worth).join(accumulated_worth).join(daily_gain)
        return tmp_df

class FundNetWorth:
    def __init__(self):
        pass