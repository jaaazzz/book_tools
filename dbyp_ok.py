#!/usr/bin/python
# coding:utf-8
import requests
import math
import random,string
import re
import time
import MySQLdb
class db_helper_class:

    def __init__(self):
        self.db = MySQLdb.connect('localhost','root','','books',charset="utf8")
        self.cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    def __del__(self):
        self.db.close()

    def exe_search(self, sql):
        # 受影响的行数
        line_cnt = self.cursor.execute(sql)
        return (line_cnt, self.cursor.fetchall())

    def exe_insert(self, sql, vals):
        self.cursor.execute(sql,vals)
        self.db.commit()

    def exe_update(self, sql, vals):
        self.cursor.execute(sql, vals)
        self.db.commit()

    def get_count(self, sql):
        ret_count = 0

        try:
            line_cnt = self.cursor.execute(sql)
            if line_cnt >= 0:
                ret_count = self.cursor.fetchall()[0].popitem()[1]
        except:
            pass

        return ret_count

    def get_cursor(self):
        return self.cursor

db_helper = db_helper_class()

input_url_file= 'my_277_name_url.txt'
ouput_name_url_file= 'xx_name_url.txt'
num_row =  1         #从第ｎ行开始读,这一行还没抓

def save(fh, contents): 
    fh.write(contents) 

def send_post(url,fh):
    # url='http://pan.baidu.com/share/transfer?shareid=2637621368&from=3527831162&ondup=newcopy&async=1&bdstoken=908ae879d2ed8fda9467b8a389a9d54e&channel=chunlei&clienttype=0&web=1&app_id=250528&logid=MTQ4ODc5MjY1Mzc4OTAuMzc4MjI1NzU0MjQ3OTc4MzM='
    #url ='https://pan.baidu.com/share/link?shareid=1137610587&uk=827180667'
    #data = {'filelist':'["/130/民国女子-桑妮"]','path':'/E-BOOK'}
    headers = { 
            "Host":"pan.baidu.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Accept":"*/*",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Referer":"http://pan.baidu.com/",
            "Origin":"http://pan.baidu.com",
            "X-Requested-With":"XMLHttpRequest"
            }
    # cookies = {'Hm_lvt_eb77799942fcf84785b5626e398e49ab':'1477534033', 'PANWEB':'1', 'bdshare_firstime':'1477546446192', 'BAIDUID':'817BD806748540F6DC7FBB04DA4D226E:FG=1', 'PSTM':'1486621023', 'BIDUPSID':'AE024330B1E6C70235D9DA2D2ED3CC1D','__cfduid':'d1395ed4b31e9c0de1980eb75d4b007a21487054573', 'BDCLND':'fUDaiKxbDnOOZmUHAqOFE2mU97DxFKCzVErYO%2Fyg%2BW8%3D', 'BDUSS':'zlWMU5rQzM3eDMta2NFRVlFWjAxTWl4NUdLMmdOUnlTYlRXRk95ZUNpZHBwZVJZSVFBQUFBJCQAAAAAAAAAAAEAAACAn6IvScTH0KnE6sTHuPbE4wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGkYvVhpGL1YT', 'STOKEN':'7f56329a1e927ceb4785bca8adeb6c2bfa195ce7b31aa23648e5814410a8e441', 'SCRC':'a326b442db9d4f8e401c7ba7bedd18c8', 'BDRCVFR[feWj1Vr5u3D]':'I67x6TjHwwYf0', 'PSINO':'3', 'H_PS_PSSID':'1423_21092_18559_17001_22035_20718', 'TOPMSG':'1488788417-0', 'Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0':'1488512892,1488512914,1488512966,1488787396', 'Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0':'1488788760', 'cflag':'15%3A3', 'PANPSC':'14667899248130652069%3ASzpdS1fQcptwreDICxvVoV9F54R%2BwEhesB0MjiMJFOW61ll3BBlDiIoMll4j7yuo4c9hfQLwDQkNSgtD0Mp7oSQaInMCgWjNTw1nodrBGAjqnomfr6U8X1CWgK6L8TsPlANdbjVx0gaCzr5I%2F7Ky%2BAwBc3CIaTTjePth2nAgN8k7LpLTMOoLpW1RXDZJ9BU%2Bo7YaFcYDR0o%3D'}
    #cookies={'BAIDUID':'1E23FDAFF46C75E23788A834AD3EE8D4:FG=1', 'BIDUPSID':'1D3BA4E1704B1E6343173798FA24E780', 'PSTM':'1472630270', 'PANWEB':'1', 'Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0':'1488508952,1488509240,1488792761', 'bdshare_firstime':'1482483557577', 'cflag':'15%3A3', 'Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0':'1488792812', 'BDUSS':'tsYnhIQ3BwZThoZHBxNmx6aW41Z25lQ2I3dnZZQWktQzE3U2lyQ3VDbjh1ZVJZSVFBQUFBJCQAAAAAAAAAAAEAAACAn6IvScTH0KnE6sTHuPbE4wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPwsvVj8LL1Yfm', 'STOKEN':'a38b42d22ba7d6e63922d8a0502aaab0c6b09990772c0e827ef8e86a66ef0cd7', 'SCRC':'c03c4a14bd08e3801c12973bc86376b0', 'PANPSC':'15608789015072789639%3ASzpdS1fQcptwreDICxvVoV9F54R%2BwEhesB0MjiMJFOW61ll3BBlDiIoMll4j7yuo4c9hfQLwDQkNSgtD0Mp7oSQaInMCgWjNjUlE1R9db62u0j%2F6OwkyrFCWgK6L8TsPlANdbjVx0gaCzr5I%2F7Ky%2BAwBc3CIaTTjePth2nAgN8k7LpLTMOoLpW1RXDZJ9BU%2Bo7YaFcYDR0o%3D'}
    #cookies={'Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492680295', 'PANWEB':'1', 'bdshare_firstime': '1477546446192', 'BAIDUID':'5D0D8CBB1B1F1D1BFED59987D7B1D571:FG=1', 'PSTM':'1486621023', 'BIDUPSID':'5D0D8CBB1B1F1D1BFED59987D7B1D571', '__cfduid':'d1395ed4b31e9c0de1980eb75d4b007a21487054573', 'BAIDUCUID':'++', 'BDUSS':'gtcjJLbXA3YUpiYnRuSUhzbjFoOWlSLTNtaG5QTzkxQUV2NDJGSVhLRTBmUTFaSVFBQUFBJCQAAAAAAAAAAAEAAACAn6IvScTH0KnE6sTHuPbE4wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADTw5Vg08OVYUH', 'STOKEN':'86365d4a9d8ce3555129ecd3f95c1390f595dc34666a5914e5e70260d61dab61', 'SCRC':'0d4863e52975c07eee4c093b19471530', 'MCITY':'-218%3A131%3A', 'BDCLND':'hLSt5io%2FRXs3JE5RiZ6GQ65jevJXyrTWK6TuWiA%2BeNk%3D', 'PSINO':'3', 'H_PS_PSSID':'22584_1449_13551_21079_20928', 'BDORZ':'B490B5EBF6F3CD402E515D22BCDA1598', 'cflag':'15%3A3', 'Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492495694,1492582088,1492655551,1492659464', 'Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492680295', 'PANPSC':'17836206781265819113%3ASzpdS1fQcptwreDICxvVoV9F54R%2BwEhesB0MjiMJFOW61ll3BBlDiIoMll4j7yuo4c9hfQLwDQkNSgtD0Mp7oSQaInMCgWjNIs1ZjqAristCiiXTA3hB5FCWgK6L8TsPlANdbjVx0gaCzr5I%2F7Ky%2BAwBc3CIaTTjePth2nAgN8k7LpLTMOoLpffsbJHGVn%2BX8KSTqGvGNRtB3EPxj2dwcPmggF7lfJq7','cflag':'15%3A3'}
    
    cookies={'Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492680293', 'PANWEB':'1', 'BAIDUID':'7FF92D4D8B54EB4C0614EAC2580607A2:FG=1',  'Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492680293','cflag':'15%3A3','PSTM':'1492681159','H_PS_PSSID':'22583_1463_21088_17001_20719','BIDUPSID':'5D0D8CBB1B1F1D1BFED59987D7B1D571','BDORZ':'B490B5EBF6F3CD402E515D22BCDA1598'}
##################################################BAIDUID=E879CB2AC96923AF412B0B5EA54E3CBB:FG=1; BIDUPSID=5D0D8CBB1B1F1D1BFED59987D7B1D571; PSTM=1492667121; PANWEB=1; PSINO=3; H_PS_PSSID=22584_1449_13551_21079_20928; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1492674803; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1492676268
    #####PANWEB=1; BAIDUID=E879CB2AC96923AF412B0B5EA54E3CBB:FG=1; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1492680295; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1492680295; cflag=15%3A3
    #PANWEB=1; BAIDUID=4691DA60B5F38C9F8C57AD21DCB57FFD:FG=1; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1492681053; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1492681053; PSTM=1492681159; H_PS_PSSID=22583_1463_21088_17001_20719; BIDUPSID=5D0D8CBB1B1F1D1BFED59987D7B1D571; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598
    resp = requests.post(url=url, cookies=cookies,headers=headers)
    filename = re.findall('<title>(.*?)</title>', resp.content)  
    print filename[0]+'||'+url+"\n"
    save(fh,filename[0]+'||'+url)
    e_filename = '_'.join(filename[0].split('_')[:-1])
    sql = 'update formal_book_info set url = %s where name =%s'
    vals = (url , e_filename)
    db_helper.exe_update(sql,vals)

#根据url文件，获取对应的书名，输出url书名文件，并保存到数据库
# file = open(input_url_file)
# fh = open(ouput_name_url_file, 'a+') 
# i=0
# while 1:
#     i=i+1
#     print i
#     if i < num_row:
#         url = file.readline()
#         pass
#     else: 
#         time.sleep(0.8)
#         url = file.readline()
#         if not url:
#             break
#         send_post(url,fh)
#根据url书名文件，将url书名存到数据库
file = open(input_url_file)
while 1:
    url = file.readline()
    if not url:
        break
    filename = url.split('||')
    e_filename = '_'.join(filename[0].split('_')[:-1])
    print e_filename
    sql = 'update formal_book_info set url = %s where name =%s'
    vals = (filename[1] , e_filename)
    db_helper.exe_update(sql,vals)









