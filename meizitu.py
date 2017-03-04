#!/usr/bin/env python　　　#在Ｌｉｎｕｘ下可以直接执行
# -*- coding: utf-8 -*-　　#解决中文出错问题

"""
Created on Mon Feb 27 20:38:41 2017

@author: ohlala

http://cuiqingcai.com/3179.html
"""
import datetime
import sys
import os
from bs4 import BeautifulSoup
from Download import request ##导入模块变了一下
from pymongo import MongoClient

class meizitu():
    def __init__(self):
        client = MongoClient()
        db = client['meinvxiezhen']
        self.meizitu_collection = db['meizitu']
        self.title = ''
        self.url = ''
        self.img_urls = []
        
    def aaa(self, all_url):
        #all_url = 'http://www.mzitu.com/all' 
        start_html = request.get(all_url, 3)  #使用另一个模块里的类的一个实例的方法
        #打印出start_html (请注意，concent是二进制的数据，一般用于下载图片、视频、音频、等多媒体内容是才使用concent, 对于打印网页内容请使用text)
        #print(start_html.text)
       
        #使用BeautifulSoup来解析我们获取到的网页‘lxml’是指定的解析器  注意ｔｅｘｔ不是ｔｘｔ
        Soup = BeautifulSoup(start_html.text, 'lxml')
    
        #‘find’ 只查找给定的标签一次，就算后面还有一样的标签也不会提取出来
        #而‘find_all’ 是在页面中找出所有给定的标签！有十个给定的标签就返回十个（返回的是个list)
        #意思是先查找 class为 all 的div标签，然后查找所有的<a>标签。
        all_a = Soup.find('div', class_='all').find_all('a')
    
        for a in all_a:
            title = a.get_text()    #取出a标签的文本
            self.title = title   #局部变量不能在其他方法中使用，所以需要self.title
            print("开始保存",title)
            path = str(title).replace('?','_')
            self.mkdir(path)    
            href = a['href']        #取出a标签的href 属性
            self.url = href
            if self.meizitu_collection.find_one({'主题地址':href}): #查看是否在数据库中
                print("该主题已保存过")
            else:              
                self.html(href)
    
    def html(self, href): #这个函数是处理套图地址获得图片的页面地址
        html = request.get(href, 3)
        html_Soup = BeautifulSoup(html.text, 'lxml')    
        max_span =  html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        page_num = 0
        for page in range (1, int(max_span)+1):
            page_url = href + '/' + str(page)
            page_num += 1
            self.img(page_url, max_span, page_num)
    
    def img(self, page_url, max_span, page_num):  #这个函数处理图片页面地址获得图片的实际地址
        img_html = request.get(page_url, 3)
        img_Soup = BeautifulSoup(img_html.text, 'lxml')
        img_url = img_Soup.find('div', class_='main-image').find('img')['src'] #字典，另ＴＭ注意 － _
        self.img_urls.append(img_url)
        print('.',end='')
        sys.stdout.flush()        #立刻输出缓存区
        if int(max_span) == page_num:
            self.save(img_url)
            post = {
                '标题':self.title, '主题地址':self.url,
                '图片地址':self.img_urls, '获取时间':datetime.datetime.now()
                }
            self.meizitu_collection.save(post)  #插入数据库！！！！！
            print('数据库插入成功')
        else:
            self.save(img_url)
    
    def save(self, img_url):  #这个函数保存图片
        name = img_url[-9:-4]
        img = request.get(img_url, 3)
        f = open(name + 'jpg', 'ab') #创建文件，写入多媒体文件必须要 b 这个参数！
        f.write(img.content)    #多媒体文件要是用conctent！
        f.close()

    def mkdir(self, path):    #这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join("/home/ohlala/meizitu", path))
        if not isExists:
            print("创建了一个名字叫做",path,"的文件夹！")
            os.makedirs(os.path.join("/home/ohlala/meizitu", path)) #创建文件夹
        os.chdir("/home/ohlala/meizitu/" + path)    #转换目录

Meizt = meizitu()
Meizt.aaa('http://www.mzitu.com/all')