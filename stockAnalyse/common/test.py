'''
Created on 2015年5月17日

@author: fufei
'''
import string
import time
import urllib.request

from bs4 import BeautifulSoup


def basicTest():
    a = {'2015':[{'name':'tom','age':'20'},{'name':'john','age':'21',"child":2}],
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
    # d = '-----'
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
    htmlstr = '''
        <DL><p>
                <DT><A HREF="http://10.27.129.242:8080/arsys/shared/login.jsp?/arsys/" ADD_DATE="1417434861" LAST_MODIFIED="1418908311">BMC Remedy Mid Tier 8.0 - Login</A>
                <DT><A HREF="http://10.27.223.144:8000/console/" ADD_DATE="1417434861" LAST_MODIFIED="1418908311">BMC Capacity Optimization</A>
                <DT><A HREF="https://10.27.131.150/bca-networks/main/displayTop.do" ADD_DATE="1417434861" LAST_MODIFIED="1418908311">BMC Network Automation</A>
                </DL>
    '''
    soup = BeautifulSoup(htmlstr)
    print(str(soup))
    anchors = soup.find_all("a")
    for a in anchors:
        print(a)
        url = a["href"]
        if(url.find("14")>=0):
            a.decompose()
    print(str(soup))


def m1(name,*args):
    print("in method m1")
    for x in args:
        print(x)
    print(name,args)

def m2(name,*args):
    print("in method m2")
    print(name,args)
    m1(name,*args)

m2("ff","a","b","c")

m2("gg")