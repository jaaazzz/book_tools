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
sql = "select id from formal_book_info where tags is not null and tags!=''"
books_ava = db_helper.exe_search(sql)
books_ids = books_ava[1]
tags = {}

#   TODO 每页创建 一个线程
#   TODO 分析每页循环取出每篇文章的内容等

for id in books_ids:
    sql = 'select * from formal_book_info where id ='+str(id['id'])
    books_info = db_helper.exe_search(sql)
    book_tag = books_info[1][0]['tags']
    print book_tag
    tags_arr = book_tag.split('|')
    for tag_i in tags_arr:
        if(tags.has_key(tag_i)):
            tags[tag_i] = tags[tag_i]+1
        else:
            tags[tag_i] = 1
for key in tags:
    sql = 'insert into tags (tag_name,num) values (%s,%s)'
    vals = (key,tags[key])
    db_helper.exe_insert(sql,vals)
