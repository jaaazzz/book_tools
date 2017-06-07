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
import shutil

book_dir = 'I:/formal_books/xx_6000/'
#book_dir = 'E:/wmv_single/'
doc = u"E:/python_workspace/book_tools/add_shudan_to_dir/书单.doc"
png = u"E:/python_workspace/book_tools/add_shudan_to_dir/书单.png"
doc1 = u'/书单.doc'
png1 = u'/书单.png'

list_file = os.listdir(book_dir) #列出文件夹下所有的目录与文件
for i in range(0,len(list_file)):
    #time.sleep(1)
    path = book_dir+list_file[i]
    print i
    if(os.path.isdir(path)):
    	shutil.copyfile(doc.encode('gbk'),path+doc1.encode('gbk'))
    	shutil.copyfile(png.encode('gbk'),path+png1.encode('gbk'))