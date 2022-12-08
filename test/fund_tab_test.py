import sys, os
import time
from threading import Thread
from loguru import logger
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
sys.path.append(os.getcwd())
from tt_web.fund import Fund
from config_files.fund_param import FUND_SEARCH_URL, MAX_THREAD_NUM
from tt_web.fund_search import CrackEastMoney
'http://fund.eastmoney.com/010331.html',
'http://fund.eastmoney.com/517280.html',
'http://fund.eastmoney.com/010422.html',
'http://fund.eastmoney.com/517550.html',
'http://fund.eastmoney.com/002967.html',
'http://fund.eastmoney.com/000056.html',

def get_fund_list():
    fund1 = Fund('110022', 'http://fund.eastmoney.com/110022.html', '易方达消费行业股票')
    fund2 = Fund('110022', 'http://fund.eastmoney.com/010331.html', '易方达消费行业股票')
    fund3 = Fund('110022', 'http://fund.eastmoney.com/517280.html', '易方达消费行业股票')
    fund4 = Fund('110022', 'http://fund.eastmoney.com/010422.html', '易方达消费行业股票')
    fund5 = Fund('110022', 'http://fund.eastmoney.com/517550.html', '易方达消费行业股票')
    fund6 = Fund('110022', 'http://fund.eastmoney.com/002967.html', '易方达消费行业股票')
    fund7 = Fund('110022', 'http://fund.eastmoney.com/000056.html', '易方达消费行业股票')
    return [fund1, fund2, fund3, fund4, fund5, fund6, fund7]

def test_open_close_tab():
    a = CrackEastMoney(FUND_SEARCH_URL.format(key='消费'), 'EastMoney.log')
    a.fund_list = get_fund_list()
    a.get_fund_data([(By.ID, "IncreaseAmount"), (By.ID, "quotationItem_DataTable"), (By.CLASS_NAME, "quotationItem_left")])


if __name__ == '__main__':
    test_open_close_tab()
                    
    