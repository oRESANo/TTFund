from lxml import etree

def get_fund_list():
    g=etree.parse('/media/caoxiangxing/6T/TTFund/test/fund_list.html',etree.HTMLParser())
    result = []
    result.append(g.xpath('//a[@data-more="jj"]/text()'))
    print(result[0])

def get_fund_details():
    g=etree.parse('/media/caoxiangxing/6T/TTFund/test/fund_details.html',etree.HTMLParser())
    # ret = g.xpath('//li[@id="increaseAmount_stage"]//td/h3/text()')
    ret = g.xpath('//li[@class="position_shares"]//td[@class="alignLeft"]/a/text()')
    # ret = g.xpath('//li[@class="position_shares"]/div[@class="poptableWrap"]//td[@class="alignRight bold"]/text()')
    # ret = g.xpath('//li[@id="position_shares"]//div[@class="poptableWrap_footer"]//a/@href')
    
    # for r in ret:
    #     print(float(r[:-1])/100)
        
    print(ret)


if __name__ == '__main__':
    get_fund_details()