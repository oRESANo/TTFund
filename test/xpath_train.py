from lxml import etree
import pandas as pd

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
    net_worth_link = etree_content.xpath('//div[@id="Div2"]//div[@class="item_more"]/a/@href')
    print(fund_quartile_rank)
    print(holding_stock_list)
    print(percentage_list)
    print(tmp)
    print(net_worth_link)

def get_fund_networth():
    etree_content=etree.parse('/media/caoxiangxing/6T/TTFund/test/fund_networth.html',etree.HTMLParser())
    fund_date = etree_content.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[1]/text()')  
    unit_net_worth = etree_content.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[2]/text()')
    accumulated_worth = etree_content.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[3]/text()')
    daily_return = etree_content.xpath('//table[@class="w782 comm lsjz"]/tbody/tr/td[4]/text()')
    current_page = etree_content.xpath('//div[@class="pagebtns"]/label[@class="cur"]/text()')
    final_page = etree_content.xpath('//div[@class="pagebtns"]/label[7]/text()')
    net_worth_label = etree_content.xpath('//div[@class="boxitem w790"]/h4/label')
    fund_date = pd.DataFrame(fund_date, columns=['date'])
    unit_net_worth = pd.DataFrame(unit_net_worth, columns=['unit_net_worth'])
    accumulated_worth = pd.DataFrame(accumulated_worth, columns=['accumulated_net_worth'])
    daily_return = pd.DataFrame(daily_return, columns=['daily_return'])
    return fund_date, unit_net_worth, accumulated_worth, daily_return

def create_networth_df():
    net_worth = pd.DataFrame(columns=['date', 'unit_net_worth', 'accumulated_net_worth', 'daily_return'])
    fund_date, unit_worth, accumulated_worth, daily_return = get_fund_networth()
    tmp_df = fund_date.join(unit_worth).join(accumulated_worth).join(daily_return)
    for _ in range(2):
        net_worth = pd.concat([net_worth,
                    tmp_df],
                    ignore_index=True)
    net_worth.unit_net_worth = net_worth.unit_net_worth.astype(float)
    net_worth.accumulated_net_worth = net_worth.accumulated_net_worth.astype(float)
    net_worth.daily_return = net_worth.daily_return.replace(r'(.*)%',  r'\1', regex=True).astype(float)/100

if __name__ == '__main__':
    # get_fund_details()
    # get_fund_networth()
    create_networth_df()