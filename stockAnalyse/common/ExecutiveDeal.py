'''
Created on 2015年5月27日

@author: fufei
'''

import http.client
from urllib.parse import unquote

httpClient = None
edInfo = [] #高管增减持信息
class ExecutiveDealInfo():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.transactedDate = '' #交易日期
        self.stockCode = '' #股票代码
        self.stockName = '' #股票简称
        self.transactedUser = '' #变动人
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
        self.stockCode2 = ''#带后缀".SH"和".SZ"的股票代码
    
    def toString(self):
        s = '[交易日期：{6}，股票代码：{0}，股票简称：{1}，变动股数：{2}，成交价格：{3}，变动金额：{4}元，变动比率:{5}]'
        s = s.format(self.stockCode,self.stockName,self.transactedVolume,self.transactedPrice,
                 self.turnover,self.ratio,self.transactedDate)
        return s

def fetchExecutiveDealInfo():
    try:
        httpClient = http.client.HTTPConnection("datainterface.eastmoney.com",80,timeout=60)
        httpClient.request('GET', '/EM_DataCenter/JS.aspx?type=GG&sty=GGMX&p=1&ps=2000&js=(x)')
        res = httpClient.getresponse()
#         print (res.status,res.reason)        
        if res.status == 200:
            data = res.readall().decode(encoding="utf-8", errors="strict")
            l = data.split('"')
            l = [x for x in l if (x!='' and x!=',')]#去掉分割字符后生成的''和','
            #获取高管增减持信息
            for e in l:            
                edi = ExecutiveDealInfo()
                l2 = e.split(",")
                edi.ratio = float(l2[0])
                edi.executiveName = l2[1]
                edi.stockCode = l2[2]
                if('002219'==edi.stockCode):
                    print(l2,l2[8])
                edi.transactedUser = l2[3]
                edi.stockType = l2[4]
                edi.transactedDate = l2[5]
                edi.transactedVolume = int(l2[6])
                edi.afterHoldings = l2[7]
                edi.transactedPrice = float(l2[8])
                edi.stockName = l2[9]
                edi.relation = l2[10]
                edi.reason = l2[12]
                edi.turnover = float(l2[13])
                edi.position = l2[14]
                edi.stockCode2 = l2[15]
                
                edInfo.append(edi)
    except Exception as err:
        print (err)
    finally:
        if httpClient:
            httpClient.close()
def findAddingAction(vol_,turnover_):
    for ed in edInfo:
       if(ed.transactedVolume>=vol_ and ed.turnover>=turnover_):
           print(ed.toString())
fetchExecutiveDealInfo()
findAddingAction(0,1000000)