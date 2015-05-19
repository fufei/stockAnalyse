'''
Created on 2015年5月17日

@author: fufei
'''
import string

from bs4 import BeautifulSoup


def basicTest():
    a = {'2015':[{'name':'tom','age':'20'},{'name':'john','age':'21'}],
    '2016':[{'name':'tom','age':'20'},{'name':'john','age':'21'}]}
    
    print(a['2015'][0]['name'])
    a['2017']=[]
    a['2017'].append({'name':'tom','age':'20'})
    a['2017'].append({'name':'john','age':'21'})
    
    print(len(a['2017']))
    
    b = {}
    b['name'] = 'b'
    print(b)
    
    c = '123.56'
    # d = '----'
    print(float(c))
    
    class BigDealRecord():
        def __init__(self,stockCode_):
            self.stockCode = stockCode_
            self.stockName = ''
    
    bd = BigDealRecord('2323')
    bd.stockName = 'sdsd'
    bd.abc = 'sds'
    
    e = 'abc'
    print(bd.stockCode)
    setattr(bd,e,'aaa')
    print(bd.abc)

def testBSOUP4():
    sibling_soup = BeautifulSoup("<a><b class='2'>text1</b><b>text2</b><c>text3</c></b></a>")
    print(sibling_soup.b.nextSibling)
    print(int(sibling_soup.b['class'][0]))
    
testBSOUP4()