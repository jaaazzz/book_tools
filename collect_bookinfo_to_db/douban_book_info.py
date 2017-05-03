#!/usr/bin/python
# coding:utf-8
import requests
import math
import random,string
import re
import time
import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取一条数据库。
data = cursor.fetchone()

# 关闭数据库连接
db.close()
books_name = 'xxurl.txt'
ouput_name_url_file= 'xx_name_url.txt'
num_row =  2295         #从第ｎ行开始读,这一行还没抓

def save(fh, contents): 
    fh.write(contents) 

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
    print book_info

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
    print intro
    print tags
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
    print comments
#get_info_by_name('谈话的力量')
get_introtag_by_url('https://book.douban.com/subject/1183730/')
#get_comments_by_url('https://book.douban.com/subject/1183730/comments')

book_name = []
book_mate_data = []
for name in book_name:
    