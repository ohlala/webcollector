#!/usr/bin/env python　　
# -*- coding: utf-8 -*-　　

"""
Created on Mon Feb 27 20:38:41 2017

@author: ohlala

http://cuiqingcai.com/3179.html
"""

import os
import requests
from bs4 import BeautifulSoup


class Meizitu():
    def all_url(self, url):     #作为对象试图使用类的方法时，如果没有ｓｅｌｆ则会参数数目不对
        all_url = url
        start_html = request(all_url)
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
            print("开始保存",title)
            path = str(title).replace('?','_')
            mkdir(path)    
            href = a['href']        #取出a标签的href 属性
            html(href)
    
    def request(self, url):   #这个函数获取网页的response 然后返回
        headers = {'User-Agent':"Mozilla/5.0(Window NT 6.1; WOW) AppleWeb Kit\
        /537.1(KHTML, like Gecko) Chrome/22.0.1207 Safari/537.1"}  #浏览器请求头
        content = requests.get(url, headers = headers)
        return content
    
    def html(self, href): #这个函数是处理套图地址获得图片的页面地址
        html = request(href)
        html_Soup = BeautifulSoup(html.text, 'lxml')    
        
        max_span =  html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range (1, int(max_span)+1):
            page_url = href + '/' + str(page)
            img(page_url)
    
    def img(self, page_url):  #这个函数处理图片页面地址获得图片的实际地址
        img_html = request(page_url)
        img_Soup = BeautifulSoup(img_html.text, 'lxml')
        img_url = img_Soup.find('div', class_='main-image').find('img')['src'] #字典，另ＴＭ注意 － _
        save(img_url)
    
    def save(self, img_url):  #这个函数保存图片
        name = img_url[-9:-4]
        img = request(img_url)
        f = open(name + 'jpg', 'ab') #创建文件，写入多媒体文件必须要 b 这个参数！
        f.write(img.content)    #多媒体文件要是用conctent！
        f.close()
    
    def mkdir(self, path):    #这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join("/home/ohlala/meizitu", path))
        if not isExists:
            print("创建了一个名字及叫做",path,"的文件夹！")
            os.makedirs(os.path.join("/home/ohlala/meizitu", path)) #创建文件夹
        os.chdir(os.path.join("/home/ohlala/meizitu", path))    #转换目录
    
    def aaa(self, b):
        print('jkhdkajh')
        print(b)
Mzitu = Meizitu() ##实例化
Mzitu.all_url('http://www.mzitu.com/all') ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）