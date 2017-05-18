# coding:utf-8
#
#2017-05-13 更新功能
#1,有些广告图片不是123456.png，根据图片大小，格式，类型去清除
#2，有些广告文字没有在<p><p>之间，在转完后再将全文中的‘行行’，qq号，网址进行替换
#3,扩大替换范围，不止html，还有htm,xhtml
#4,添加断点续转功能，之前转过的就不转了
import zipfile  
import os
import chardet
import re
from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('GBK')

mark = '本书由“行行”整理，如果你不知道读什么书或者想获得更多免费电子书请加小编微信或QQ：491256034  小编也和结交一些喜欢读书的朋友  或者关注小编个人微信公众号id：d716-716  为了方便书友朋友找书和看书，小编自己做了一个电子书下载网站，网址：www.ireadweek.com  QQ群：550338315'
mymark = '本书由“极刻”整理，书籍下载可登录网站：极刻分享“www.jikeshare.com” 。网站海量书籍不断更新，提供优质的文学/工具/小说类资源。若链接失效或书籍查找可加小编微信:/QQ:1504227550 '
new_temp_file = 'E:/python_workspace/book_tools/new.html'
log_name = 'clean_epub.log'
book_rootdir = u'J:/books/417_xx/'
after_clean_epub_dir = 'J:/books/epub514/'

def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()
def clean_epub(file_name,after_clean_epub_dir):  
   # """unzip zip file"""  
    try:
        zip_file = zipfile.ZipFile(file_name) 

        if os.path.isdir(file_name + "_files"):  
            pass  
        else:  
            os.mkdir(file_name + "_files")  
        for names in zip_file.namelist():  
            zip_file.extract(names,file_name + "_files/")  
        zip_file.close()  
        search_html(file_name+'_files/')
        zip_dir(file_name+'_files',after_clean_epub_dir+os.path.basename(file_name))
    except Exception,e :
        print e

def search_html(rootdir):
    for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in  filenames:                       #输出文件夹信息
            if(os.path.splitext(filename)[1]=='.html' or os.path.splitext(filename)[1]=='.htm' or os.path.splitext(filename)[1]=='.xhtml'):
                    parent = parent.strip('/')+'/'
                    clean_html(filename,parent)
            #删除广告图片
            if(os.path.splitext(filename)[1]=='.png' or os.path.splitext(filename)[1]=='.jpg' or os.path.splitext(filename)[1]=='.jpeg'):
                fp = open(parent.strip('/') + '/' + filename,'rb')
                im = Image.open(fp)
                fp.close()
                hw = im.size
                if(((hw[0] == 628) and (hw[1] == 760)) or (filename == '123456.jpeg')):
                    os.remove(parent.strip('/') + '/' + filename)

def clean_html(filename,rootdir):
    all_the_text = open(rootdir+filename).read()
    if((all_the_text.find('www.ireadweek.com')!=-1) and (all_the_text.find('25岁前一定要读的25本书')!=-1)):
        fo = open(rootdir+filename, "w+")
        new_txt = open(new_temp_file).read()
        fo.write(new_txt)
        fo.close()
        log(log_name,rootdir+filename,'replace_file')
    elif ((all_the_text.find('www.ireadweek.com')!=-1) and (all_the_text.find('25岁前一定要读的25本书')==-1)):
            #参考,标签之内和标签之外的广告
            #all_ps_out = re.findall('<(.*?)>(.*?)</(.*?)>',new_txt,re.S)
            #all_ps_out = re.findall('</(.*?)>(.*?)<(.*?)>',new_txt,re.S)
            all_ps = re.findall('<p(.*?)>(.*?)</p>',all_the_text,re.S)
            new_txt = all_the_text
            for p in all_ps:
                if len(p)>1:
                    if(p[1].find('www.ireadweek.com')!=-1):
                        global the_p
                        the_p = p[1]
                        new_txt = new_txt.replace(the_p,mymark)
            if(new_txt.find('123456.jpeg')!=-1):
                new_txt = new_txt.replace('123456.jpeg','')

            #最后对文件进行一次替换
            if(new_txt.find('行行')!=-1):
                new_txt = new_txt.replace('行行','极刻')
            if(new_txt.find('491256034')!=-1):
                new_txt = new_txt.replace('491256034','1504227550')
            if(new_txt.find('d716-716')!=-1):
                new_txt = new_txt.replace('d716-716','')
            if(new_txt.find('www.ireadweek.com')!=-1):
                new_txt = new_txt.replace('www.ireadweek.com','www.jikeshare.com')
            if(new_txt.find('550338315')!=-1):
                new_txt = new_txt.replace('550338315','')     
            if(new_txt.find('2338856113')!=-1):
                new_txt = new_txt.replace('2338856113','1504227550')
            if(new_txt.find('幸福的味道')!=-1):
                new_txt = new_txt.replace('幸福的味道','')     
            if(new_txt.find('周读')!=-1):
                new_txt = new_txt.replace('周读','极刻')         
            fo = open(rootdir+filename, "w+")
            fo.write(new_txt)
            fo.close() 
            log(log_name,rootdir+filename,'replace_str')
    else:   
            if(all_the_text.find('123456.jpeg')!=-1):
                all_the_text = all_the_text.replace('123456.jpeg','')

            #最后对文件进行一次替换
            if(all_the_text.find('行行')!=-1):
                all_the_text = all_the_text.replace('行行','极刻')
            if(all_the_text.find('491256034')!=-1):
                all_the_text = all_the_text.replace('491256034','1504227550')
            if(all_the_text.find('d716-716')!=-1):
                all_the_text = all_the_text.replace('d716-716','')
            if(all_the_text.find('www.ireadweek.com')!=-1):
                all_the_text = all_the_text.replace('www.ireadweek.com','www.jikeshare.com')
            if(all_the_text.find('550338315')!=-1):
                all_the_text = all_the_text.replace('550338315','')     
            if(all_the_text.find('2338856113')!=-1):
                all_the_text = all_the_text.replace('2338856113','1504227550')
            if(all_the_text.find('幸福的味道')!=-1):
                all_the_text = all_the_text.replace('幸福的味道','')     
            if(all_the_text.find('周读')!=-1):
                all_the_text = all_the_text.replace('周读','极刻')         
            fo = open(rootdir+filename, "w+")
            fo.write(all_the_text)
            fo.close() 
            log(log_name,rootdir+filename,'replace_str')

def log(log_name,filename,str1):
    fb = open(log_name,"a+")
    fb.write(filename+'||'+str(str1)+'\n')

for parent,dirnames,filenames in os.walk(book_rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for filename in  filenames:                       #输出文件夹信息
        if(os.path.splitext(filename)[1]=='.epub'):
            file_path = parent.strip('/')+'/'+filename
            after_name = after_clean_epub_dir.strip('/')+'/'+filename
            try:
                print filename
            except:
                print '11'
            if(os.path.exists(after_name)):
                print 'have'
            else:
                clean_epub(file_path,after_clean_epub_dir)
