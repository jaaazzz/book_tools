#coding=utf-8
#更新20170514
#1修复带特殊字符的标签导入出错
#2导入图片地址改为本地地址
#
import sys
# import urllib
# import urllib2
# import cookielib
from tools import *
import json
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(2000)
# default_encoding = 'utf-8'
# if sys.getdefaultencoding() != default_encoding:
#     reload(sys)
#     sys.setdefaultencoding(default_encoding)

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
        self.cursor.execute(sql)
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
# todo 尝试使用 scrapy


wp_url = "http://127.0.0.1/wordpress/wp-json/wp/v2/posts"
wp_url_tags = "http://127.0.0.1/wordpress/wp-json/wp/v2/tags"
username = "admin"
password = "nXej0MIUHEzb3tJetCHsEGjF"

# ready_cate_id = "4"
#ready_cate_id = "10"
wp_data = {}
wp_headers = {}
old_tags = {}


# todo 先获取所有的 old tags
old_tags = Crawl_helper_tools_url.http_auth_handle_get_tag(wp_url_tags,wp_data)
if (old_tags == "fail"):
    print('获取标签失败')
    sys.exit()
print('已经存在的标签列表：')
# print(old_tags)
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer' : 'http:www.share345.com'}

sql = 'select id from formal_book_info where douban_name is not null'
db_helper = db_helper_class()
books_ava = db_helper.exe_search(sql)
books_ids = books_ava[1]

#   TODO 每页创建 一个线程
#   TODO 分析每页循环取出每篇文章的内容等

for id in books_ids:
    sql = 'select * from formal_book_info where id ='+str(id['id'])
    books_info = db_helper.exe_search(sql)
    wp_data['status'] = "publish"
    wp_data['title'] = books_info[1][0]['name']
    comments = books_info[1][0]['comments']
    pic_url = books_info[1][0]['pic_url'].split('||')
    pic_url = '/wp-content/uploads/2017/05/db_'+pic_url[1]+'.jpg'
    try:
        comments_arr = comments.split('|')
        comments_str = ''
        for item in comments_arr:
            comments_str = comments_str + '<p>'+ item + '</p>'
    except:
        comments_str = ''
    tmp_content ='''<div class="article_content" id="article_content" style="">
    <div class='book_name' style='width:100%;height:50px;'>
        <div style='width:5px;height:1em;background-color:#4499ee;float:left;margin-top:5px;margin-right:15px'></div>
        <p>'''+books_info[1][0]['name']+'''</p>
    </div>
    <hr>
    <div class="book_info">
        <div style="float:left;height:200px;width:150px">
            <img style="height:200px;width:150px" src="'''+pic_url+'''"/>
        </div>
        <div class="details" style='margin-left:160px;height:200px;width:400px'>
            <p style='margin-bottom:5px'>作者：'''+books_info[1][0]['author']+'''</p>
            <p style='margin-bottom:5px'>标签：'''+books_info[1][0]['tags']+'''</p>
            <p style='margin-bottom:5px'>豆瓣评分：'''+books_info[1][0]['douban_score']+'''分</p>
            <div>
                <button class='b_download'><a href=''>点击下载</a></button>
                <button class='b_keyword' onclick='get_keyword()'>获取密码</button>
                <a id='password'></a>
                <p style='color:red'>注：如果下载失败，请联系小编，微信或QQ：1504227550</p>
            </div>
        </div>
    </div>
    <hr>
    <div class='intro'>
        <p>简介：</p>
        <p>'''+books_info[1][0]['intro']+'''</p>
    </div>
    <hr>
    <div class='abstra'>
        <p>简评 ：</p>'''+ comments_str +'''
    </div>
    <hr>
    <div class='menu'>
    </div>
</div>
<script>
function get_keyword(){
    document.getElementById("password").innerHTML="";
}
</script>'''
    wp_data['content'] = tmp_content
    wp_data['author'] = 1
    # wp_data['author'] = books_info[1][0]['author']
    #wp_data['slug'] = books_info[1][0]['name']
    #wp_data['slug'] = md5(time() . mt_rand(1,1000000));
    wp_data['o_author_new_field'] = books_info[1][0]['author']
    wp_data['score_new_field'] = books_info[1][0]['douban_score']
    wp_data['book_link_new_field'] =''
    wp_data['categories[0]'] = books_info[1][0]['category']
    page_tags = books_info[1][0]['tags'].split('|')
    for i_page_tag in page_tags:
        if old_tags.has_key(i_page_tag):
            print('tag 存在')
            print(old_tags[i_page_tag])
        else:
            print('tag 不存在')
            #print(i_page_tag)
            #todo 不存在创建tag
            res = Crawl_helper_tools_url.http_auth_handle_create_tag(username,password,wp_url_tags,i_page_tag,wp_headers)
            print res
            if (res != "fail"):
                decode_res_create_tag = json.loads(res)
                #print decode_res_create_tag[u'id']+i_page_tag
                old_tags[i_page_tag] = decode_res_create_tag[u'id']
    for tag_i in range(len(page_tags)):
        #print(page_tags[tag_i])
        # print(old_tags)
        # wp_data["tags["+str(tag_i)+"]"] = old_tags[page_tags[tag_i].decode('utf-8')]
        try:
            wp_data["tags["+str(tag_i)+"]"] = old_tags[page_tags[tag_i]]
        except:
            pass
    #print wp_data
    res = Crawl_helper_tools_url.http_auth(username,password,wp_url,wp_data,wp_headers)
    print 'add wenzhang'
    print res
    if (res == "fail"):
        print("添加失败")
    # sys.exit()

