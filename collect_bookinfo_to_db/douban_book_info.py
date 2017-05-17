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

def get_info_by_name(name):
    name = clean_book_name(name)
    book_info = {}
    url = 'https://book.douban.com/subject_search?search_text='+name
    headers = { 
            "Host":"book.douban.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Accept":"*/*",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
            }
    #cookies={'Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492680293', 'PANWEB':'1', 'BAIDUID':'7FF92D4D8B54EB4C0614EAC2580607A2:FG=1',  'Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0':'1492680293','cflag':'15%3A3','PSTM':'1492681159','H_PS_PSSID':'22583_1463_21088_17001_20719','BIDUPSID':'5D0D8CBB1B1F1D1BFED59987D7B1D571','BDORZ':'B490B5EBF6F3CD402E515D22BCDA1598'}
    cookies = {'bid':'CBLU4pblNlA', 'gr_user_id':'c95c3a9f-c831-47e0-b9c7-74255a165eef', '_pk_id.100001.3ac3':'ffbfe42e72b4262e.1493000558.1.1493000944.1493000558.','_pk_ses.100001.3ac3':'*','gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03':'83e0bee1-14a5-41af-804c-aed46e585656','gr_cs1_83e0bee1-14a5-41af-804c-aed46e585656':'user_id%3A0'}
    # proxies = { "http": "http://124.42.7.103:80"}
    #豆瓣的这个url，只能用get来获取
    time.sleep(0.5)
    resp = requests.get(url=url, cookies=cookies, headers=headers)
    #print resp.content
    #re.S 让 . 可以匹配换行符
    book_items = re.findall('<li class="subject-item">(.*?)</li>', resp.content,re.S)
    try:
        url_name = re.findall('<a href="(.*?)" title="(.*?)"(.*?)>',book_items[0] ,re.S)

        #print book_info['url']
        try :
            book_info['url'] = url_name[0][0]
        except:
            book_info['url'] = ''
        try:
            book_info['real_name'] = url_name[0][1]
        except:
            book_info['real_name'] = ''
        book_info['pub'] = re.findall('<div class="pub">(.*?)</div>',book_items[0] ,re.S)
        try:
            book_info['pub'] = book_info['pub'][0].replace("\n", "").strip()
        except:
            book_info['pub'] = ''
        book_info['pl'] = re.findall('<span class="pl">(.*?)</span>',book_items[0] ,re.S)
        try:
            book_info['pl'] = book_info['pl'][0].replace("\n", "").strip()
        except:
            book_info['pl'] = ''
        book_info['author'] = book_info['pub'].split('/')
        if(len(book_info['author'])>1):
            book_info['author'] = book_info['author'][0]
        else:
            book_info['author'] = ''
    except:
        book_info = {}
    print book_info
    return book_info

def get_info_by_url(url):
    info = {}
    tags = []
    headers = { 
            "Host":"book.douban.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Accept":"*/*",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
            }   
    cookies = {'bid':'CBLU4pblNlA', 'gr_user_id':'c95c3a9f-c831-47e0-b9c7-74255a165eef', '_pk_id.100001.3ac3':'ffbfe42e72b4262e.1493000558.1.1493000944.1493000558.','_pk_ses.100001.3ac3':'*','gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03':'83e0bee1-14a5-41af-804c-aed46e585656','gr_cs1_83e0bee1-14a5-41af-804c-aed46e585656':'user_id%3A0'}
    #proxies = { "http": "http://124.42.7.103:80"}
    time.sleep(0.5)
    resp = requests.get(url=url, cookies=cookies, headers=headers)
    intro = re.findall('<div class="intro">(.*?)<p>(.*?)</p></div>',resp.content,re.S)
    tags_info = re.findall('<a class="  tag" href="(.*?)">(.*?)</a>',resp.content,re.S)
    score = re.findall('<strong class="ll rating_num " property="v:average">(.*?)</strong>',resp.content,re.S)
    pic_url = re.findall('<a class="nbg"(.*?)href="(.*?)"(.*?)</a>',resp.content,re.S)
    for x in tags_info:
        tags.append(x[1])
    tags = '|'.join(tags)
    try :
        #有展开更多时，取第二条
        if(len(intro)>1):
            info['intro'] = intro[1][1]
        else:
            info['intro'] = intro[0][1]
    except Exception,e:
        print 'intro',e
        info['intro'] = ''
    info['tags'] = tags
    try :
        info['score'] = score[0]
    except Exception,e:
        print 'score',e
        info['score'] = ''
    try: 
        time.sleep(0.5)
        #pic= requests.get(url=info['pic_url'], cookies=cookies, headers=headers, timeout=120)
        #print pic
        ids = url.strip('/').split('/')
        ids = ids[-1]
        #下载图片，图片以书的id命名
        info['pic_url'] = pic_url[0][1] +'||' +str(ids)
        pic_name =  'db_' + str(ids)+ '.jpg'

        #可以注释掉，用download_book_pic.py去下载
        urllib.urlretrieve(info['pic_url'],pic_stroe+pic_name)  
        time.sleep(1) #每下一张，休息5秒，防止被封  
        #print '%s\n' %u  

        # fp = open(pic_stroe+pic_name,'wb')
        # fp.write(pic.content)
        # fp.close()
    except Exception,e:
        print 'pic_url',e
        info['pic_url'] = ''
    return info
def get_comments_by_url(url):
    url = url.strip('/') +'/comments/'
    comments_arr = []
    headers = { 
            "Host":"book.douban.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Accept":"*/*",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
            }   
    cookies = {'bid':'CBLU4pblNlA', 'gr_user_id':'c95c3a9f-c831-47e0-b9c7-74255a165eef', '_pk_id.100001.3ac3':'ffbfe42e72b4262e.1493000558.1.1493000944.1493000558.','_pk_ses.100001.3ac3':'*','gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03':'83e0bee1-14a5-41af-804c-aed46e585656','gr_cs1_83e0bee1-14a5-41af-804c-aed46e585656':'user_id%3A0'}
    #proxies = { "http": "http://124.42.7.103:80"}
    time.sleep(0.5)
    resp = requests.get(url=url, cookies=cookies, headers=headers)
    total_num = re.findall('<span id="total-comments">全部共(.*?)条</span>',resp.content,re.S)
    if(int(total_num[0])==0):
        return ''
    page_num = int(total_num[0])/20
    if(page_num>5):
        page_num = 5
    else:
        for page in range(1,page_num+2):
            url = url + 'hot?p=' +str(page)
            time.sleep(0.5)
            resp = requests.get(url=url, cookies=cookies, headers=headers)
            info_arr = re.findall('<li class="comment-item"(.*?)<span class="user-stars allstar(.*?) rating"(.*?)<p class="comment-content">(.*?)</p>',resp.content,re.S)
            for item in info_arr:
                if(item[1]=='40' or item[1]=='50'):
                    comments_arr.append(item[3])
        print comments_arr
        if  len(comments_arr)>5:
            comments_arr.sort(key = len ,reverse=True)
            comments_arr = comments_arr[:5]
        return '|'.join(comments_arr)
def clean_book_name(book_name):
    book_name = re.subn('\((.*?)\)','',book_name)
    book_name = book_name[0]
    return book_name
def cate_by_tags(tags):
    print tags
    if(len(tags)>0):
        sql = 'select id ,tag from cate_tag'
        cate_tag = db_helper.exe_search(sql)
        cate_tag = cate_tag[1]
        max = 0 #未分类
        id = 1
        for item in cate_tag:
            arr = item['tag'].split('|')        
            #tmp = [val for val in tags if val in arr]
            tmp = list(set(arr).intersection(set(tags)))
            if(len(tmp)>max):
                max = len(tmp)
                id = item['id']
    print id
    return id
#get_info_by_name('谈话的力量')
#get_introtag_by_url('https://book.douban.com/subject/1183730/')
#get_comments_by_url('https://book.douban.com/subject/1183730/comments')

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
