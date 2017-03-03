# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 20:03:16 2017

@author: ohlala
"""

import requests
#import re
import random
import time
from bs4 import BeautifulSoup

class Download:
    def __init__(self):
        self.iplist = [] 
        html = requests.get("http://haoip.cc/tiqu.htm")
        
        Soup = BeautifulSoup(html.text, 'lxml')
        ipli = Soup.find('div', class_='col-xs-12').get_text().split(' ')
        while '' in ipli:
                ipli.remove('')
        while '\n' in ipli:
                ipli.remove('\n')
        for i in ipli:
            self.iplist.append(i[:-1])
            
#        iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
#        for ip in iplistn:
#            i = re.sub('\n', '', ip)  ##re.sub 是re模块替换的方法，这儿表示将\n替换为空
#            self.iplist.append(i.strip())  ##添加到我们上面初始化的list里面
 
            
        self.user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    def get(self, url, timeout, proxy=None, num_retries=1):
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent': UA}        
        if proxy == None:
            try:
                return requests.get(url, headers=headers, timeout=timeout)
            except:
                print('b')
                print(proxy, num_retries)
                if num_retries > 0:
                    print ('获取网页出错，１０秒后将重试倒数第', num_retries, '次')                    
                    time.sleep(10)
                    return self.get(url, timeout, None, num_retries-1 )  #???
                else:
                    print('开始使用代理')
                    time.sleep(10)
                    IP = random.choice(self.iplist)
                    proxy = {'http': IP}
                    return self.get(url, timeout, proxy)  #???
        else:
            try:
                IP = random.choice(self.iplist)
                proxy = {'http': IP}
                return requests.get(url, proxies=proxy, headers=headers, timeout=timeout)
            except:
                if num_retries > 0:
                    print ('正在更换代理，１０秒后讲重试倒数第', num_retries, '次')                    
                    print ('当前代理是', proxy)
                    time.sleep(10)
                    return self.get(url, timeout, proxy, num_retries-1)  #???
                else:
                    print('使用代理也不行了')
                    time.sleep(10)
                    return self.get(url, 3)
request = Download()
