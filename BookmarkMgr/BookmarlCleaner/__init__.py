import fileinput
from pathlib import Path, PurePath
import re
import os
import json
import urllib.request

from bs4 import BeautifulSoup

urls = {}
def touchURL(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding':'gzip,deflate',
               'Connection':'close',
               #'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
               }
    request = urllib.request.Request(url)
    for x,y in headers.items():
        request.add_header(x, y)    
    request.method = "HEAD"
    return urllib.request.urlopen(request,timeout=5)

def cleanBookMarks(folder):
    for child in folder["children"]:
        if(child.__contains__('children')):#是1个folder
            cleanBookMarks(child)
        elif(child.__contains__('uri')):#是1个书签
            url = child['uri']
            title = child['title']
            if(re.match("https?://", url)):#排除指向本地系统的书签
                #排除不需要检查的URL，例如指向局域网的书签
                if(len(exclusions)>0):
                    matched = False
                    for e in exclusions:
                        if(url.find(e)>=0):
                            matched = True
                            break
                    if(matched):
                        continue  
                
                try:
#                     print(url,title)
                    res = touchURL(url)
                    urls[url]=title
                except Exception as err:
                    print(err,url,title)
                    folder["children"].remove(child)

def cleanBookmarksInJSONFormat(inpath,outpath):
    infile = open(inpath, mode='r', encoding='utf-8')
    if(os.path.exists(outpath)):
        os.remove(outpath)
    outfile = open(outpath, mode='x', encoding='utf-8')
    try:
        data = json.load(infile)
        for item in data['children']:
            guid = item['guid']
            #如果是书签菜单、书签工具栏和未分类书签，进去清理里面的书签
            if(guid.find("menu")>=0 or guid.find("toolbar")>=0 or guid.find("unfiled")>=0):
                print(item['title'])
                if(item.__contains__('children')):
                    cleanBookMarks(item)
        json.dump(data,outfile,ensure_ascii=False)
    finally:
        infile.close()
        outfile.close()

def cleanBookmarksInHTMLFormat(inpath,outpath):
    infile = open(inpath, mode='r', encoding='utf-8')
    if(os.path.exists(outpath)):
        os.remove(outpath)
    outfile = open(outpath, mode='x', encoding='utf-8')
    count = 0
    try:
        soup = BeautifulSoup(infile.read())
        anchors = soup.find_all("a",href=re.compile("https?://"))
                
        for a in anchors:
            count += 1   
            url = a['href']
            #排除不需要检查的URL
            if(len(exclusions)>0):
                matched = False
                for e in exclusions:
                    if(url.find(e)>=0):
                        matched = True
                        break
                if(matched):continue
                
            try:
                res = touchURL(url)
            except Exception as err:
                print(err,url,a.get_text()) 
                a.decompose()
          
        print("found "+str(count)+" links")
        outfile.write(str(soup))
    finally:
        infile.close()
        outfile.close()

inpath = "C:/Users/fufei/Documents/bookmarks-2015-05-24.json"
dirName = os.path.dirname(inpath)
outpath = dirName+"/resultbk.json"
exclusions = ("cnpc","//10.","//11.","w3")
cleanBookmarksInJSONFormat(inpath,outpath)