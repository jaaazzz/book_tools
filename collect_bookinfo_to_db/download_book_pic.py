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
import urllib
from PIL import Image

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

pic_stroe = 'D:/xampp/htdocs/wordpress/wp-content/uploads/2017/05/'


#根据数据库中的图片url下载图片
sql = "select id,pic_url from formal_book_info where pic_url is not null and pic_url !=''"
num = db_helper.exe_search(sql)
ids = num[1]
for id in ids:
    pic_arr = id['pic_url'].split('||')
    pic_name =  'db_' + pic_arr[1]+ '.jpg'
    print pic_stroe + pic_name
    if(os.path.exists(pic_stroe + pic_name)):
        try:
            fp = open(pic_stroe + pic_name,'rb')
            im = Image.open(fp)
            fp.close()
        except Exception,e :
            fp.close()
            os.remove(pic_stroe + pic_name)
            urllib.urlretrieve(pic_arr[0],pic_stroe+pic_name)  
            time.sleep(5) #
    else:
        urllib.urlretrieve(pic_arr[0],pic_stroe+pic_name)  
        time.sleep(5) #     
   