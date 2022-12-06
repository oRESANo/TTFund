import numpy as np

FUND_SEARCH_URL = 'http://fund.eastmoney.com/data/fundsearch.html?spm=search&key={key}#key{key}'



def cal_gaussian_ratio():
    avg_value = 0
    sigma = 1
    x = np.array([-2, -1, -0.5, 0, 0.5, 1, 2])
    y = np.multiply(np.power(np.sqrt(2 * np.pi) * sigma, -1), np.exp(-np.power(x - avg_value, 2) / 2 * sigma ** 2))
    return y


FUND_RANK_PARAM = cal_gaussian_ratio()
FUND_RANK_PERIOD = np.array(['1week', '1month', '3months', '6months', '1year', '2years', '3years'])