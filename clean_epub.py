#!/usr/bin/python
# coding:utf-8
import zipfile  
import os
import chardet
import re
import sys
reload(sys)
sys.setdefaultencoding('GBK')

mark = '本书由“行行”整理，如果你不知道读什么书或者想获得更多免费电子书请加小编微信或QQ：491256034  小编也和结交一些喜欢读书的朋友  或者关注小编个人微信公众号id：d716-716  为了方便书友朋友找书和看书，小编自己做了一个电子书下载网站，网址：www.ireadweek.com  QQ群：550338315'
mymark = '本书由“极刻”整理，书籍下载可登录网站：极刻分享“www.jikeshare.com” 。网站海量书籍不断更新，提供优质的文学/工具/小说类资源。若链接失效或书籍查找可加小编微信:/QQ:1504227550 '
new_temp_file = 'E:/python_work_space/book_tools/new.html'
log_name = 'clean_epub.log'
book_rootdir = 'E:/xx_417/'
after_clean_epub_dir = 'E:/epub/'

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

def search_html(rootdir):
    for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in  filenames:                       #输出文件夹信息
            if(os.path.splitext(filename)[1]=='.html'):
                    parent = parent+'/'
                    clean_html(filename,parent)

def clean_html(filename,rootdir):
    all_the_text = open(rootdir+filename).read()
    if((all_the_text.find('www.ireadweek.com')!=-1) and (all_the_text.find('25岁前一定要读的25本书')!=-1)):
        fo = open(rootdir+filename, "w+")
        new_txt = open(new_temp_file).read()
        fo.write(new_txt)
        fo.close()
        log(log_name,rootdir+filename,'replace_file')
    elif ((all_the_text.find('www.ireadweek.com')!=-1) and (all_the_text.find('25岁前一定要读的25本书')==-1)):
            all_ps = re.findall('<p class="(.*?)">(.*?)</p>',all_the_text,re.S)
            for p in all_ps:
                if len(p)>1:
                    if p[1].find('www.ireadweek.com'):
                        the_p = p[1]
            new_txt = all_the_text.replace(the_p,mymark)
            print new_txt
            fo = open(rootdir+filename, "w+")
            fo.write(new_txt)
            fo.close() 
            log(log_name,rootdir+filename,'replace_str')
    else:   
        pass

def log(log_name,filename,str1):
    fb = open(log_name,"a+")
    fb.write(filename+'||'+str(str1)+'\n')

for parent,dirnames,filenames in os.walk(book_rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for filename in  filenames:                       #输出文件夹信息
        if(os.path.splitext(filename)[1]=='.epub'):
            file_path = parent+'/'+filename
            file_path = file_path
            clean_epub(file_path,after_clean_epub_dir)
