import pandas as pd
import os, sys
from collections import OrderedDict
print(sys.path.append(os.getcwd()))
from selenium_base.web_base import WebPage
from config_files.fund_param import FUND_RANK_PARAM, FUND_RANK_PERIOD

class Fund(WebPage):
    def __init__(self):
        super.__init__(self)
        self.fund_code = None
        self.fund_name = None
        self.hoding_stock_list = pd.DataFrame(columns=['stock_name', 'holding_percentage'])
        self.net_worth = pd.DataFrame(columns=['date', 'unit_net_worth', 'accumulated_net_worth', 'daily_return'])
        # 优秀-4， 良好-3， 一般-1， 较差-0 (0-25%, 25-50%, 50-75%, 75-100%) | @ 1 week, 1 month, 3months, 6months, from year begin, 1 year, 2 years, 3 years
        self.quartile_rank = OrderedDict()
        # [(rank, total_num)...] | @ 1week, 1month, 3months, 6months, from year begin, 1 year, 2 years, 3 years
        self.rank_at_same_category = []
        self.top_10_holding_percetage = None
        
    def fund_rank_score(self):
        if self.quartile_rank:
            for rank in self.quartile_rank:
                self.fund_score = 