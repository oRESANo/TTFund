from lxml import etree

def get_fund_list():
    g=etree.parse('/media/caoxiangxing/6T/TTFund/test/fund_list.html',etree.HTMLParser())
    result = []
    result.append(g.xpath('//a[@data-more="jj"]/text()'))
    print(result[0])

def get_fund_details():
    etree_content=etree.parse('/media/caoxiangxing/6T/TTFund/test/fund_details.html',etree.HTMLParser())
    fund_quartile_rank = etree_content.xpath('//li[@id="increaseAmount_stage"]//td/h3/text()')
    holding_stock_list = etree_content.xpath('//li[@class="position_shares"]//td[@class="alignLeft"]/a/text()| //li[@class="position_shares"]//td[@class="alignLeft"]/div/text()')
    percentage_list = etree_content.xpath('//li[@class="position_shares"]/div[@class="poptableWrap"]//td[@class="alignRight bold"]/text()')
    tmp = []
    for percentage in percentage_list:
        if percentage[-1] == '%':
            tmp.append(float(percentage[:-1])/100)
        else:
            pass
    net_worth_link = etree_content.xpath('//li[@id="position_shares"]//div[@class="poptableWrap_footer"]//a/@href')
    print(fund_quartile_rank)
    print(holding_stock_list)
    print(percentage_list)
    print(tmp)
    print(net_worth_link)

def get_fund_networth():
    etree_content=etree.parse('/media/caoxiangxing/6T/TTFund/test/fund_networth.html',etree.HTMLParser())
    # /html/body/div[1]/div[8]/div[3]/div[2]/div[3]/div/div[2]/div/div[2]/table/tbody/tr[1]/td[1]
    fund_date = etree_content.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[1]/text()')  
    unit_worth = etree_content.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[2]/text()')
    accumulated_worth = etree_content.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[3]/text()')
    daily_gain = etree_content.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[4]/text()')
    # next_page_button = etree_content.xpath('//div[@class="pagebtns"]//input[@type="button]')
    print(fund_date)
    print(unit_worth)
    print(accumulated_worth)
    print(daily_gain)
    # print(next_page_button)

if __name__ == '__main__':
    # get_fund_details()
    get_fund_networth()