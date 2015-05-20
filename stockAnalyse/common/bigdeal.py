'''
Created on 2015年5月17日

@author: fufei

'''
import http.client
from bs4 import BeautifulSoup

httpClient = None
colName = ['transactedDate','stockCode','stockName','transactedDetail','currentPrice',
           'transactedPrice','transactedVolume','turnover','buyer','seller']
bigDealInfo = {}

class BigDealRecord():
   
    def __init__(self):
        self.transactedDate = '' #交易日期
        self.stockCode = '' #股票代码
        self.stockName = '' #股票简称
        self.transactedDetail = '' #交易详情
        self.currentPrice = 0 #当前价格
        self.transactedPrice = 0 #成交价格
        self.transactedVolume = 0 #成交数量
        self.turnover = 0 #成交金额
        self.buyer = '' #买方营业部
        self.seller = '' #卖方营业部
        self.ratio = -1000000
    
    def calRatio(self):
        #（成交价格-当前价格）/当前价格
        if(self.currentPrice != 0 and self.transactedPrice !=0):
            self.ratio = (self.transactedPrice - self.currentPrice)/self.currentPrice
        else:
            self.ratio = -1000000 #如果没有当前价格和成交价格，ratio设为大负值
    
    def toString(self):
        s = '[股票代码：{0}，股票简称：{1}，当前价格：{2}，成交价格：{3}，成交量：{4}万股，成交金额：{5}万元,比率:{6}]'
        s = s.format(self.stockCode,self.stockName,self.currentPrice,self.transactedPrice,
                 self.transactedVolume,self.turnover,self.ratio)
        return s
        
def fetchPartOfDealingInfo(td,bdr):
    if(not td.text == '--'):
        bdr.transactedPrice = float(td.text)
    else:
        bdr.transactedPrice = 0;
                    
    td = td.nextSibling.nextSibling
    if(not td.text == '--'):
        bdr.transactedVolume = float(td.text)
    else:
        bdr.transactedVolume = 0
                    
    td = td.nextSibling.nextSibling
    if(not td.text == '--'):
        bdr.turnover = float(td.text)     
    else:
        bdr.turnover = 0   
    
    td = td.nextSibling.nextSibling
    bdr.buyer = td.text
    
    td = td.nextSibling.nextSibling
    bdr.seller = td.text

def fetchAllBigDealingInfo():
    try:
        httpClient = http.client.HTTPConnection("data.eastmoney.com",80,timeout=60)
        httpClient.request('GET', '/dzjy/default.html')
        res = httpClient.getresponse()
        print (res.status,res.reason)
        
        if res.status == 200:
            soup = BeautifulSoup(res.readall())
            tbody = soup.find('th',text="交易日期").parent.parent 
            #Get the big deal info
            transactedDate = ''
            stockCode = ''
            stockName = ''
            currentPrice = 0
            for tr in tbody.find_all('tr',class_="list_eve"):
                bdr = BigDealRecord()             
                td = tr.td
                if(td.has_attr('valign')):#如果是显示交易时间的cell
                    transactedDate = td.text
#                     print(transactedDate)
                    bigDealInfo[transactedDate]=[]
                    td = td.nextSibling.nextSibling #两个nextSibling是为了跳过NavigableString对象
                    if(transactedDate=='2015-05-12'):
                        ss = 'dd'
                        
                if td.has_attr('rowspan'):
                    stockCode = td.text
                    bdr.stockCode = stockCode
                    
                    td = td.nextSibling.nextSibling 
                    stockName = td.text    
                    bdr.stockName = stockName  
                                  
                    td = td.nextSibling.nextSibling.nextSibling.nextSibling
                    if(not td.text == '--'):
                        currentPrice = float(td.text)    
                    else:
                        currentPrice = 0;                                  
                    bdr.currentPrice = currentPrice
                    td = td.nextSibling.nextSibling
                    fetchPartOfDealingInfo(td, bdr)
                else:
                    bdr.stockCode = stockCode
                    bdr.stockName = stockName  
                    bdr.currentPrice = currentPrice                    
                    fetchPartOfDealingInfo(td, bdr)
                bdr.calRatio()
                bigDealInfo[transactedDate].append(bdr)
    except Exception as err:
        print (err)
    finally:
        if httpClient:
            httpClient.close()
    print(list(bigDealInfo.keys()))

def findTargetStock(ratio,volume):
    for transactedDate in sorted(bigDealInfo.keys(),reverse=True):
        print(transactedDate)
        for bigDealRecord in bigDealInfo[transactedDate]:
#             print(bigDealRecord.toString())
            if(bigDealRecord.ratio>=ratio and bigDealRecord.turnover>volume):
                print(bigDealRecord.toString())           

fetchAllBigDealingInfo()
findTargetStock(0.01,1000)
