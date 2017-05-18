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

#2017-05-14 更新
#1过滤怪异标签.不过滤了，怪异标签较少
#2过滤差评
#3下载图片

#TODO
#搜书名的时候，有时候取不到搜索列表中的第一个结果，如十个词汇里的中国
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

book_dir = 'E:/wmv/'
pic_stroe = 'D:/xampp/htdocs/wordpress/wp-content/uploads/2017/05/'
format = 'txt|pdf|epub|mobi'
cate = ''


def clean_book_name(book_name):
    book_name = re.subn('\((.*?)\)','',book_name)
    book_name = book_name[0]
    return book_name



#汇集信息，包括分类
list_file = os.listdir(book_dir) #列出文件夹下所有的目录与文件
for i in range(0,len(list_file)):
    #time.sleep(1)
    path = book_dir+list_file[i]
    print path
    list_file[i] = list_file[i].decode('GBK').encode('utf8')
    sql = "select id from formal_book_info where name = '"+list_file[i]+"'"
    num = db_helper.get_count(sql)
    if(num==0):
        print list_file[i]
        if os.path.isdir(path):
            book_info1 = get_info_by_name(list_file[i])
            try:
                book_info2 = get_info_by_url(book_info1['url'])
                book_info3 = get_comments_by_url(book_info1['url'])
                tags_arr = book_info2['tags'].split('|')
                cate = cate_by_tags(tags_arr)
                sql = "insert into formal_book_info (name,douban_name,format,author,tags,category,intro,comments,datetime,pic_url,douban_score) \
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                fld_inserttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))

                vals = (
                    list_file[i],
                    book_info1['real_name'],
                    format,
                    book_info1['author'],
                    book_info2['tags'],
                    cate,
                    book_info2['intro'],
                    book_info3,
                    fld_inserttime,
                    book_info2['pic_url'],
                    book_info2['score']
                )
                # 实时入库
                db_helper.exe_insert(sql, vals)
            except Exception,e:
                print e
                sql = "insert into formal_book_info (name,format,datetime) \
                    values (%s,%s,%s)"
                fld_inserttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
                vals = (
                    list_file[i],
                    format,
                    fld_inserttime
                )    
                db_helper.exe_insert(sql, vals)
    else:
        print 'have'

#单独分类,对没分类的书分类，已分类的保持不变
# sql = "select id,tags,category from formal_book_info where tags is not null and tags !=''"
# num = db_helper.exe_search(sql)
# ids = num[1]
# for id in ids:
#     if(id['category'] == '1'):
#         tags_arr = id['tags'].split('|')
#         cate = cate_by_tags(tags_arr)
#         sql = 'UPDATE formal_book_info SET category = %s WHERE id = %s'
#         vals = (cate,id['id'])
#         db_helper.exe_update(sql,vals)
