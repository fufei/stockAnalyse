'''
Created on 2015年5月24日

@author: fufei
'''
import unittest
from BookmarlCleaner import *

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testTouchurl(self):
        res = touchURL("http://www.csdn.net")
        self.assertEqual(200, res.status, "error")
        self.assertEqual("OK", res.reason, "error")
        
    def testCleanBookMarks(self):
        testStr = {
            "guid": "KHR1sYnNMjIY",
            "title": "English",
            "children": [{
                "guid": "k4_DneZ1IJdI",
                "title": "OuHua Dictionary and Translation",
                "uri": "http://www.ohdict.com/?"
            },
            {
                "guid": "-KiGfnmcBmdZ",
                "title": "最近使用的标签",
                "uri": "place:type=6&sort=14&maxResults=10"
            },           
            {
                "guid": "asdawe234",
                "title": "内网",
                "uri": "http://10.11.11.11/wed/a/"
            },           
            {
                "guid": "234234sfrser",
                "title": "听力每日练习-音频类型-在线英语听力列表",
                "uri": "http://www.ebigear.com/ResHtml/3/301/"
            },           
            {
                "guid": "ZaIQYS2234234",
                "title": "金山词霸",
                "uri": "http://djw.iciba12.com/"
            }]
        }
        exclusion = ("cnpc","//10.","//11.","w3")
        cleanBookMarks(testStr,*exclusion)
        print(urls)
        outpath = "c:/Users/fufei/Documents/testbm.json"
        if(os.path.exists(outpath)):
            os.remove(outpath)
        json.dump(testStr,open(outpath,mode='x'),ensure_ascii=False)
        self.assertEqual(2, len(urls),"error")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()