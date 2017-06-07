#!/usr/bin/python
# coding:utf-8
import requests
import math
import random,string
import re
import time
import MySQLdb
import sys
class db_helper_class:

    def __init__(self):
        self.db = MySQLdb.connect('localhost','root','','wordpress',charset="utf8")
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

sql = "select post_content from wp_posts where post_title !='' and post_content is not null"
result = db_helper.exe_search(sql)
for item in result[1]:
    item['post_content']
    

