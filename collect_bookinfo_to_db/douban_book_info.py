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

    #**********************************************************************
    # 描  述： 数据库查询操作
    #
    # 参  数： sql, 查询语句
    #
    # 返回值： 返回一个元组，包含受影响的行数、及fetchall()迭代器
    # 修  改：
    #**********************************************************************
    def exe_search(self, sql):
        # 受影响的行数
        line_cnt = self.cursor.execute(sql)
        return (line_cnt, self.cursor.fetchall())

    #**********************************************************************
    # 描  述： 数据库insert插入操作
    #
    # 参  数： sql, 插入格式部分
    # 参  数： vals, 插入值元组
    #
    # 返回值： 空
    # 修  改：
    #**********************************************************************
    def exe_insert(self, sql, vals):
        self.cursor.execute(sql)
        self.db.commit()

    #**********************************************************************
    # 描  述： update操作
    #
    # 参  数： sql, 查询语句
    #
    # 返回值： 空
    # 修  改： 
    #**********************************************************************
    def exe_update(self, sql, vals):
        self.cursor.execute(sql, vals)
        self.db.commit()

    #**********************************************************************
    # 描  述： 获取select count计数值
    #
    # 参  数： sql, sql语句
    #
    # 返回值： 计数值
    # 修  改： 
    #**********************************************************************
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

book_dir = ''
format = 'txt|pdf|epub|mobi'

def get_info_by_name(name):
    book_info = {}
    url = 'https://book.douban.com/subject_search?search_text='+name
    headers = { 
            "Host":"book.douban.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Accept":"*/*",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
            }
    print url 
    #cookies={'Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492680293', 'PANWEB':'1', 'BAIDUID':'7FF92D4D8B54EB4C0614EAC2580607A2:FG=1',  'Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492680293','cflag':'15%3A3','PSTM':'1492681159','H_PS_PSSID':'22583_1463_21088_17001_20719','BIDUPSID':'5D0D8CBB1B1F1D1BFED59987D7B1D571','BDORZ':'B490B5EBF6F3CD402E515D22BCDA1598'}
    cookies = {'bid':'CBLU4pblNlA', 'gr_user_id':'c95c3a9f-c831-47e0-b9c7-74255a165eef', '_pk_id.100001.3ac3':'ffbfe42e72b4262e.1493000558.1.1493000944.1493000558.','_pk_ses.100001.3ac3':'*','gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03':'83e0bee1-14a5-41af-804c-aed46e585656','gr_cs1_83e0bee1-14a5-41af-804c-aed46e585656':'user_id%3A0'}
    #豆瓣的这个url，只能用get来获取
    resp = requests.get(url=url, cookies=cookies, headers=headers)
    #print resp.content
    #re.S 让 . 可以匹配换行符
    book_items = re.findall('<li class="subject-item">(.*?)</li>', resp.content,re.S)  
    url_name = re.findall('<a href="(.*?)" title="(.*?)"(.*?)>',book_items[0] ,re.S)
    #print book_info['url']
    book_info['url'] = url_name[0][0]
    book_info['real_name'] = url_name[0][1]
    book_info['pub'] = re.findall('<div class="pub">(.*?)</div>',book_items[0] ,re.S)
    book_info['pub'] = book_info['pub'][0].replace("\n", "").strip()
    book_info['pl'] = re.findall('<span class="pl">(.*?)</span>',book_items[0] ,re.S)
    book_info['pl'] = book_info['pl'][0].replace("\n", "").strip()
    book_info['author'] = book_info['pub'].split('/')
    if(len(book_info['author'])>1):
        book_info['author'] = book_info['author'][0]
    else:
        book_info['author'] = ''
    return book_info

def get_introtag_by_url(url):
    tags = []
    headers = { 
            "Host":"book.douban.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Accept":"*/*",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
            }   
    cookies = {'bid':'CBLU4pblNlA', 'gr_user_id':'c95c3a9f-c831-47e0-b9c7-74255a165eef', '_pk_id.100001.3ac3':'ffbfe42e72b4262e.1493000558.1.1493000944.1493000558.','_pk_ses.100001.3ac3':'*','gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03':'83e0bee1-14a5-41af-804c-aed46e585656','gr_cs1_83e0bee1-14a5-41af-804c-aed46e585656':'user_id%3A0'}
    resp = requests.get(url=url, cookies=cookies, headers=headers)
    intro = re.findall('<div class="intro">(.*?)<p>(.*?)</p></div>',resp.content,re.S)
    tags_info = re.findall('<a class="  tag" href="(.*?)">(.*?)</a>',resp.content,re.S)
    for x in tags_info:
        tags.append(x[1])
    intro =intro[0][1]
    tags = '|'.join(tags)
    return (intro,tags)
def get_comments_by_url(url):
    comments_arr = []
    headers = { 
            "Host":"book.douban.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Accept":"*/*",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
            }   
    cookies = {'bid':'CBLU4pblNlA', 'gr_user_id':'c95c3a9f-c831-47e0-b9c7-74255a165eef', '_pk_id.100001.3ac3':'ffbfe42e72b4262e.1493000558.1.1493000944.1493000558.','_pk_ses.100001.3ac3':'*','gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03':'83e0bee1-14a5-41af-804c-aed46e585656','gr_cs1_83e0bee1-14a5-41af-804c-aed46e585656':'user_id%3A0'}
    resp = requests.get(url=url, cookies=cookies, headers=headers)
    comments = re.findall('<p class="comment-content">(.*?)</p>',resp.content,re.S)
    if  len(comments)>5:
        comments = comments[:5]
    return '|'.join(comments)
#get_info_by_name('谈话的力量')
#get_introtag_by_url('https://book.douban.com/subject/1183730/')
#get_comments_by_url('https://book.douban.com/subject/1183730/comments')

list = os.listdir(book_dir) #列出文件夹下所有的目录与文件
for i in range(0,len(list)):
    path = os.path.join(rootdir,list[i])
    if os.path.isdir(path):
        book_info1 = get_info_by_name(list[i])
        if(book_info1['url']):
            book_info2 = get_introtag_by_url(book_info1['url'])
            book_info3 = get_comments_by_url(book_info1['url'])
            sql = "insert into formal_book_info (name,douban_name,format,author,tags,category,intro,comments,datetime) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            fld_inserttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))

            vals = (
                list[1],
                book_info1['real_name'],
                format,
                book_info1['author'],
                book_info2[1],
                cate,
                book_info2[0],
                book_info3,
                fld_inserttime
            )
            # 实时入库
            self.db_oper.exe_insert(sql, vals)
        else:
            sql = "insert into formal_book_info (name,format,datetime) \
                values (%s,%s,%s)"
            fld_inserttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
            vals = (
                list[1],
                format,
                fld_inserttime
            )    
            self.db_oper.exe_insert(sql, vals)