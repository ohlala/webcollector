# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':"Mozilla/5.0(Window NT 6.1; WOW) AppleWeb Kit/537.1(KHTML, like Gecko) Chrome/22.0.1207 Safari/537.1"}  
all_url = 'http://www.mzitu.com/all'
start_html = requests.get(all_url, headers=headers)
Soup = BeautifulSoup(start_html.text, 'lxml')
all_a = Soup.find('div', class_='all').find_all('a')

for a in all_a:
    title = a.get_text()
    href = a['href']
    html = requests.get(href, headers=headers)
    html_Soup = BeautifulSoup(html.text, 'lxml')
    max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
    for page in range (1, int(max_span)+1):
        page_url = href + '/' + str(page)
        img_html = requests.get(page_url, headers=headers)
        img_Soup = BeautifulSoup(img_html.text, 'lxml')
        img_url = img_Soup.find('div', class_='main-image').find('img')['src']
        name = img_url[-9:-4]
        img = requests.get(img_url, headers=headers)
        path = str(title).replace('?','_').strip()
        isExists = os.path.exists(os.path.join("/home/ohlala/meizitu", path))
        if not isExists:
            print("创建了一个名字及叫做",path,"的文件夹！")
            os.makedirs(os.path.join("/home/ohlala/meizitu", path)) #创建文件夹
        os.chdir(os.path.join("/home/ohlala/meizitu", path))    #转换目录
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close