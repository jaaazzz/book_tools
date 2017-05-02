#coding=utf-8
import sys
# import urllib
# import urllib2
# import cookielib
from tools import *
import json

# todo 尝试使用 scrapy

reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(2000)
# default_encoding = 'utf-8'
# if sys.getdefaultencoding() != default_encoding:
#     reload(sys)
#     sys.setdefaultencoding(default_encoding)
wp_url = "http://127.0.0.1/wordpress/wp-json/wp/v2/posts"
wp_url_tags = "http://127.0.0.1/wordpress/wp-json/wp/v2/tags"
username = "admin"
password = "nXej0MIUHEzb3tJetCHsEGjF"
# ready_cate_id = "4"
ready_cate_id = "10"
wp_data = {}
wp_headers = {}
old_tags = {}


# todo 先获取所有的 old tags
res_old_tags = Crawl_helper_tools_url.http_auth_handle_get_tag(wp_url_tags,wp_data)
if (res_old_tags == "fail"):
    print('获取标签失败')
    sys.exit()
decode_res_tags = json.loads(res_old_tags)
for res_tag in decode_res_tags:
    old_tags[res_tag['name']] = res_tag['id']
print('已经存在的标签列表：')
print(old_tags)

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer' : 'http:www.share345.com'}


#   TODO 每页创建 一个线程
#   TODO 分析每页循环取出每篇文章的内容等

while(i <= int(page)):
 
            wp_data['status'] = "publish"
            wp_data['title'] = page_title
            wp_data['content'] = page_content
            wp_data['author'] = 1
            wp_data['slug'] = n[-8:]
            wp_data['categories[0]'] = ready_cate_id

            for tag_i in range(len(page_tags)):
                print(page_tags[tag_i])
                print(old_tags)
                # wp_data["tags["+str(tag_i)+"]"] = old_tags[page_tags[tag_i].decode('utf-8')]
                wp_data["tags["+str(tag_i)+"]"] = old_tags[page_tags[tag_i]]
            print '333'
            res = Crawl_helper_tools_url.http_auth(username,password,wp_url,wp_data,wp_headers)
            if (res == "fail"):
                print("添加失败")
            # sys.exit()

        except Exception , e:
            print 'except some page error....',e
            continue
