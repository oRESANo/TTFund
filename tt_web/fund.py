import pandas as pd
import os, sys
import numpy as np
from collections import OrderedDict
sys.path.append(os.getcwd())
from config_files.fund_param import FUND_RANK_MULTI_PARAM, FUND_RANK_PERIOD
from tt_web.fund_sup.fund_common import fund_rank_4_convert

class Fund:
    def __init__(self, code, url, name):
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
        
    # 获取fund的四分位排名, 数据不够重置flag
    def get_fund_quartile_rank(self, fund_rank_4_list:list):
        fund_rank_4_list.pop(4)
        for rank_4 in fund_rank_4_list:
            self.quartile_rank.append(fund_rank_4_convert(rank_4))
            if rank_4 == '--':
                self.lack_data = True

    def get_fund_rank_score(self):
        self.fund_rank_score = sum(self.quartile_rank * self.rank_score_params)

class FundNetWorth:
    def __init__(self):
        pass