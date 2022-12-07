from lxml import etree

if __name__ == '__main__':
    g=etree.parse('/media/caoxiangxing/6T/TTFund/test/fund_list.html',etree.HTMLParser())
    result = []
    result.append(g.xpath('//a[@data-more="jj"]/text()'))
    print(result[0])