'''
Created on 2015年5月27日

@author: fufei
'''

import http.client
from urllib.parse import unquote

from bs4 import BeautifulSoup

from common import headers


httpClient = None
edInfo = {} #高管增减持信息
class ExecutiveDealInfo(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        self.transactedDate = '' #交易日期
        self.stockCode = '' #股票代码
        self.stockName = '' #股票简称
        self.transactedDetail = '' #变动人
        self.transactedVolume = '' #变动股数
        self.transactedPrice = 0 #成交价格
        self.turnover = 0 #变动金额
        self.reason = 0 #变动原因
        self.ratio = 0 #变动比例
        self.afterHoldings = '' #变动后持股数
        self.stockType = '' #持股种类
        self.executiveName = '' #董监高姓名
        self.position = ''#职务
        self.relation = ''#变动人与董监高关系
    
    def toString(self):
        s = '[股票代码：{0}，股票简称：{1}，变动股数：{2}，成交价格：{3}，变动金额：{4}万元，变动比率:{5}]'
        s = s.format(self.stockCode,self.stockName,self.transactedVolume,self.transactedPrice,
                 self.turnover,self.ratio)
        return s

def fetchExecutiveDealInfo():
    try:
        httpClient = http.client.HTTPConnection("datainterface.eastmoney.com",80,timeout=60)
        httpClient.request('GET', '/EM_DataCenter/JS.aspx?type=GG&sty=GGMX&p=1&ps=100')
        res = httpClient.getresponse()
#         print (res.status,res.reason)        
        if res.status == 200:
            data = res.readall().decode(encoding="utf-8", errors="strict")
            print(data)
            #获取高管增减持信息
            transactedDate = ''
            stockCode = ''
            stockName = ''
#             for tr in tbody.find_all('tr'):
#                 print(tr.get_text())
    except Exception as err:
        print (err)
    finally:
        if httpClient:
            httpClient.close()

fetchExecutiveDealInfo()