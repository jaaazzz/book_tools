#!/usr/bin/python
# coding:utf-8
import requests
import math
import random,string
import re
import time
import os
import os.path

#读出pdf
# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfpage import PDFTextExtractionNotAllowed
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.pdfdevice import PDFDevice
# from pdfminer.layout import *
# from pdfminer.converter import PDFPageAggregator



# def Pdf2Txt(Path,Save_name):
#     #来创建一个pdf文档分析器
#     parser = PDFParser(Path)
#     #创建一个PDF文档对象存储文档结构
#     document = PDFDocument(parser)
#     # 检查文件是否允许文本提取
#     if not document.is_extractable:
#         raise PDFTextExtractionNotAllowed
#     else:
#         # 创建一个PDF资源管理器对象来存储共赏资源
#         rsrcmgr=PDFResourceManager()
#         # 设定参数进行分析
#         laparams=LAParams()
#         # 创建一个PDF设备对象
#         # device=PDFDevice(rsrcmgr)
#         device=PDFPageAggregator(rsrcmgr,laparams=laparams)
#         # 创建一个PDF解释器对象
#         interpreter=PDFPageInterpreter(rsrcmgr,device)
#         # 处理每一页
#         for page in PDFPage.create_pages(document):
#             interpreter.process_page(page)
#             # 接受该页面的LTPage对象
#             layout=device.get_result()
#             for x in layout:
#                 if(isinstance(x,LTTextBoxHorizontal)):
#                     with open('%s'%(Save_name),'a') as f:
#                         f.write(x.get_text().encode('utf-8')+'\n')

# Path = open('ceshi.pdf', 'rb')
# Pdf2Txt(Path,'aa.txt')

#create pdf
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_pdf(input, output="out.pdf"):
    now = datetime.datetime.today()
    date = '2017'
    c = canvas.Canvas(output)
    textobject = c.beginText()
    textobject.setTextOrigin(inch, 11*inch)
    textobject.textLines('''Disk Capcity Report: %s''' %date)
    for line in input:
        textobject.textLine(line.strip())
    c.drawText(textobject)
    c.showPage()
    c.save()
report = ['sadfdfdfsdsffs','111111111111']
create_pdf(report)


# import sys 
# from pyPdf import PdfFileWriter, PdfFileReader
# from urllib import urlopen
# from pdfminer.pdfinterp import PDFResourceManager, process_pdf
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from io import StringIO
# from io import open

# def readPDF(pdfFile):
#     rsrcmgr = PDFResourceManager()
#     retstr = StringIO()
#     laparams = LAParams()
#     device = TextConverter(rsrcmgr, retstr, laparams=laparams)

#     process_pdf(rsrcmgr, device, pdfFile)
#     device.close()

#     content = retstr.getvalue()
#     retstr.close()
#     return content

# pdfFile = urlopen("yjw.pdf")
# outputString = readPDF(pdfFile)
# print(outputString)
# pdfFile.close()


# def mergePdfFiles(outputFile, inputFiles): 
#         output = PdfFileWriter() 
#         for inputFile in inputFiles: 
#                 print 'Adding file' + inputFile 
#                 input = PdfFileReader(file(inputFile, "rb")) 
#                 for page in input.pages: 
#                         output.addPage(page) 
#         print 'All files added' 
#         #From writer to file 
#         outputStream = file(outputFile, "wb") 
#         output.write(outputStream)
#         outputStream.close()
# if __name__ == '__main__': 
#         print 'Merging Pdf Files...' 
#         mergePdfFiles("Book.pdf", ["Part1.pdf","Part2.pdf"]) 
#         print 'Merge Completed'
