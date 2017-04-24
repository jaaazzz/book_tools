#!/usr/bin/python
# coding:utf-8
# import rarfile  
# import os  
# def un_rar(file_name):  
#    # """unrar zip file"""  
#     rar = rarfile.RarFile(file_name)  
#     if os.path.isdir(file_name + "_files"):  
#         pass  
#     else:  
#         os.mkdir(file_name + "_files")  
#     os.chdir(file_name + "_files")  
#     rar.extractall()  
#     rar.close()  
# un_rar('/var/www/python/test/1368个单词就够了-王乐平.epub')
import zipfile  
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

mark = '本书由“行行”整理，如果你不知道读什么书或者想获得更多免费电子书请加小编微信或QQ：491256034  小编也和结交一些喜欢读书的朋友  或者关注小编个人微信公众号id：d716-716  为了方便书友朋友找书和看书，小编自己做了一个电子书下载网站，网址：www.ireadweek.com  QQ群：550338315'
mymark = '111111111111111111111'
new_temp_file = '/var/www/python/book_tools/new.html'
log_name = 'clean_epub.log'
def un_zip(file_name):  
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

def search_html(rootdir):
	for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
	    for filename in  filenames:                       #输出文件夹信息
	        if(os.path.splitext(filename)[1]=='.html'):
	            clean_html(filename,rootdir)

def clean_html(filename,rootdir):
    all_the_text = open(rootdir+filename).read()
    if((all_the_text.find('www.ireadweek.com')!=-1) and (all_the_text.find('25岁前一定要读的25本书')!=-1)):
    	fo = open(rootdir+filename, "rw+")
    	new_txt = open(new_temp_file).read()
    	fo.write(new_txt)
    	fo.close()
    	log(log_name,filename,'replace_file')
    elif ((all_the_text.find('www.ireadweek.com')!=-1) and (all_the_text.find('25岁前一定要读的25本书')==-1)):
    	new_txt = all_the_text.replace(mark,mymark)
    	fo = open(rootdir+filename, "rw+")
	fo.write(new_txt)
	fo.close() 
	log(log_name,filename,'replace_str')
    else:	
    	pass

def log(log_name,filename,str1):
    fb = open(log_name,"a+")
    fb.write(filename+'||'+str(str1)+'\n')
un_zip('/var/www/python/test/1368个单词就够了-王乐平.epub')