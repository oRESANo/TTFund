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
    fund_list = []
    # fund_list.append(Fund('110022', 'http://fund.eastmoney.com/110022.html', '易方达消费行业股票'))
    # fund_list.append(Fund('009265', 'http://fund.eastmoney.com/009265.html', '易方达消费精选股票'))
    fund_list.append(Fund('006309', 'http://fund.eastmoney.com/006309.html', '汇添富全球消费混合人民币C'))
    return fund_list

def test_open_fund_list():
    a = CrackEastMoney(FUND_SEARCH_URL.format(key='消费'), 'EastMoney.log')
    a.get_fund_list((By.CLASS_NAME, "search-result"))

def test_open_close_tab():
    a = CrackEastMoney(FUND_SEARCH_URL.format(key='消费'), 'EastMoney.log')
    a.fund_list = get_fund_list()
    return a

def test_fund_score():
    fund_obj = test_open_close_tab()
    fund_obj.get_fund_data([(By.ID, "IncreaseAmount"),
                            (By.ID, "quotationItem_DataTable"),
                            ])
    
def test_window_close():
    broswer = webdriver.Chrome()
    for _ in range(3):
        broswer.switch_to.new_window('tab')
        broswer.get('http://fund.eastmoney.com/110022.html')
        # broswer.switch_to.window(broswer.window_handles[-1])
        # broswer.close()
    broswer.switch_to.window(broswer.window_handles[-1])
    broswer.close()
    print(len(broswer.window_handles))
    broswer.switch_to.window(broswer.window_handles[-1])
    broswer.close()
    print(len(broswer.window_handles))
    broswer.switch_to.window(broswer.window_handles[-1])
    broswer.close()
    print(len(broswer.window_handles))
    broswer.switch_to.window(broswer.window_handles[0])
    broswer.switch_to.new_window('tab')
    broswer.get('www.baidu.com')
    

if __name__ == '__main__':
    test_open_fund_list()
                    
    