from selenium import webdriver
from selenium.webdriver.common.by import By
from config_files.fund_param import FUND_SEARCH_URL

class CrackEastMoney():
    def __init__(self, keyword):
        self.url = FUND_SEARCH_URL
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.browser.get(self.url)
        
    def get_fund():
        pass
        
        
if __name__ == '__main__':
    
    browser = webdriver.Chrome()