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

authorize = '<div>如果本站内的资源侵犯了您的合法权益，请发送邮件至1504227550#qq.com。</div><div>小编将在看到邮件后的第一时间内删除资源！</div>'
my_intro = '<div>本书由“极刻”整理，网站海量书籍不断更新，提供优质的文学/工具/小说类资源。</div><div>若链接失效或查找指定书籍可加小编微信/QQ:1504227550或加群643890191。</div><div>如果本站内的资源侵犯了您的合法权益，请发送邮件至1504227550#qq.com。</div><div>小编将在看到邮件后的第一时间内删除资源！</div>'

my_comment_l = '''<div>小编会不定期为大家提供各类优质书单以及长期更新各类精美图书。</div>
        <p>包括：</p>
        <p style="text-indent:2em">
        豆瓣、当当、知乎主流网站推荐书籍，涵盖历史、文学、励志、青春等各个方面</p>
        <p style="text-indent:2em">各类实用工具书，如考研考证工具书，IT技术书</p>
        <p style="text-indent:2em">种类丰富的网络小说。</p>
        <div>喜欢读书的小伙伴们千万不要错过，如果喜欢我们网站，记得Ctrl+D收藏哦！</div>
        <div>如果有找不到的书籍可以加QQ或微信：1504227550，来找小编要书哦！</div>
        <div>小编整理了海量精美图书，只有你想不到，没有我们找不到！</div>'''
my_comment_s = '''<div>喜欢读书的小伙伴们如果喜欢我们网站，记得Ctrl+D收藏哦！</div>
        <div>如果有找不到的书籍可以加QQ或微信：1504227550，来找小编要书哦！</div>
        <div>小编整理了海量精美图书，只有你想不到，没有我们找不到！</div>'''

db_helper = db_helper_class()

def deal_intro(intro):
    if(len(intro)>100 and len(intro)<500):
        new_intro = intro + authorize
    if(len(intro)<100):
        new_intro = intro + my_intro
    if(len(intro)>500):
        new_intro = intro[:500] + '...</p>' + authorize
    return new_intro
def deal_comments(comments):
    new_comments = '<p>简评 ：</p>'
    single_comments = re.findall("<p>(.*?)</p>",comments,re.S)
    comments_arr = single_comments[1:]
    comments_o_arr = set(comments_arr)
    for item in comments_o_arr:
        new_comments = new_comments + item
    if(len(new_comments)>500):
        new_comments = new_comments + my_comment_s
    else:
        new_comments = new_comments + my_comment_l
    return new_comments

sql = "select ID,post_content from wp_posts where post_title !='' and post_content is not null"
result = db_helper.exe_search(sql)
#简介
#
for item in result[1]:
    intro = re.findall("<div class='intro'>(.*?)</div>",item['post_content'],re.S)
    new_intro = deal_intro(intro[0][0])
    new_post = re.sub("<div class='intro'>(.*?)</div>","<div class='intro'>"+new_intro+"</div>",item['post_content'],flags=re.S)
    comments = re.findall("<div class='abstra'>(.*?)</div>",item['post_content'],re.S)
    new_comments = deal_comments(comments[0][0])
    new_post = re.sub("<div class='abstra'>(.*?)</div>","<div class='abstra'>"+new_comments+"</div>",new_post,flags=re.S)
    sql = "update wp_posts set post_content = %s where ID = %s"
    vals = (new_post,item['ID'])
    db_helper.exe_update(sql,vals)