#!/usr/bin/python
# coding:utf-8
import requests
import math
import random,string
import re
import time
import MySQLdb
import os
import chardet
def get_info_by_name():
    url = 'http://www.ip.cn/'
    #url = 'https://www.douban.com/'
    headers = { 
            "Host":"book.douban.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Accept":"*/*",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
            }
    #cookies={'Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492680293', 'PANWEB':'1', 'BAIDUID':'7FF92D4D8B54EB4C0614EAC2580607A2:FG=1',  'Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492680293','cflag':'15%3A3','PSTM':'1492681159','H_PS_PSSID':'22583_1463_21088_17001_20719','BIDUPSID':'5D0D8CBB1B1F1D1BFED59987D7B1D571','BDORZ':'B490B5EBF6F3CD402E515D22BCDA1598'}
    cookies = {'bid':'EquU9wmwNMI', 'gr_user_id':'9c148356-2155-49cb-931d-347fecee1304', '_vwo_uuid_v2':'F1FD27F0D00E9F07BA0146F2F8C12330|f0ff6789345bc443569fdf7fb1558247','gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03':'c860e281-1ce4-4fcb-b40b-65e3f31b6fc1','gr_cs1_c860e281-1ce4-4fcb-b40b-65e3f31b6fc1':'user_id%3A0'}
    proxies = { "http": "http://175.155.25.45:808"}
    #豆瓣的这个url，只能用get来获取
    resp = requests.get(url=url, cookies=cookies, headers=headers, proxies=proxies)
    print resp.content
get_info_by_name()
