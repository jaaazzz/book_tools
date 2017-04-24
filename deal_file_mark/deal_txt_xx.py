#!/usr/bin/python
# coding:utf-8
import requests
import math
import random,string
import re
import time
import os
import os.path


rootdir = "/var/www/python/test/"                                   # 指明被遍历的文件夹

my_mark_font = "111111111111111111"

my_mark_back = "222222222222222222"

mark = "ireadweek"

log_name ='xx_clean_txt.log'
def clean_txt(my_mark_font,my_mark_back,mark,filename,rootdir):
    fo = open(rootdir+filename, "rw+")
    fb = open(rootdir+filename+'bak',"a+")
    lines = fo.readlines()
    i=0
    mark_index=[]
    for line in lines:
        print line.find(mark)
        if(line.find(mark)!=-1):
            lines[i] = my_mark_font
            mark_index.append(i)
        i=i+1
    fb.write(my_mark_font)
    for k in range(mark_index[0]+1,mark_index[1]):
        fb.write(lines[k])
    fb.write(my_mark_back)
    log(log_name,filename,len(lines),mark_index[1])
    fb.close() 
def log(log_name,filename,str1,str2):
    fb = open(log_name,"a+")
    fb.write(filename+'||'+str(str1)+'||'+str(str2)+'\n')

for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for filename in  filenames:                       #输出文件夹信息
        if(os.path.splitext(filename)[1]=='.txt'):
            clean_txt(my_mark_font,my_mark_back,mark,filename,rootdir)
