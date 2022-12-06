import pandas as pd
import os, sys
import numpy as np
from collections import OrderedDict
print(sys.path.append(os.getcwd()))
from selenium_base.web_base import WebPage
from config_files.fund_param import FUND_RANK_MULTI_PARAM, FUND_RANK_PERIOD
from tt_web.fund_sup import fund_rank_4_convert

class Fund(WebPage):
    def __init__(self):
        super.__init__(self)
        self.fund_code = None
        self.fund_name = None
        self.hoding_stock_list = pd.DataFrame(columns=['stock_name', 'holding_percentage'])
        self.net_worth = pd.DataFrame(columns=['date', 'unit_net_worth', 'accumulated_net_worth', 'daily_return'])
        # 优秀-4， 良好-3， 一般-1， 不佳-0 (0-25%, 25-50%, 50-75%, 75-100%) | @ 1 week, 1 month, 3months, 6months, from year begin, 1 year, 2 years, 3 years
        self.quartile_rank = np.array() # [4,2,1,4,0,1,3]
        self.rank_period = FUND_RANK_PERIOD # 1 week, 1 month, 3months, 6months, from year begin, 1 year, 2 years, 3 years
        self.rank_score_params = FUND_RANK_MULTI_PARAM # [0.05399097 0.24197072 0.35206533 0.39894228 0.35206533 0.24197072 0.05399097]
        self.rank_at_same_category = [] # [(rank, total_num)]
        self.top_10_holding_percetage = 0
        self.fund_rank_score = 0
        self.lack_data = False
        
    # 获取fund的四分位排名, 数据不够重置flag
    def get_fund_quartile_ranke(self, fund_rank_4_list):
        for rank_4 in fund_rank_4_list:
            self.quartile_rank.append(fund_rank_4_convert(rank_4))
        if len(self.quartile_rank) < 7:
            gap = 7- len(self.quartile_rank)
            for _ in range(gap):
                self.quartile_rank.append(0)
            self.lack_data = True
    
    def get_fund_rank_score(self):
        self.fund_rank_score = sum(self.quartile_rank * self.rank_score_params)