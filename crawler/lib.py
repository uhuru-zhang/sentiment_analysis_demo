"""
基础模块

1. simple_download(url,args={})
2. download_use_chromedriver(url,args={})
"""

import random
import requests
from selenium import webdriver


my_headers=["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
			'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
			'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
			'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
			'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ',  
			'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)']


def simple_download(url,args={}):
	"""使用requests请求，下载网页"""
	random_header = random.choice(my_headers)
	headers = {'User-Agent' : random_header}
	data = requests.get(url,headers=headers,params=args)
	data.encoding = 'utf-8'
	return data.text

def download_use_chromedriver(url,args={}):
	"""调用chromedriver，爬取网页"""
	driver = webdriver.Chrome() # 需要对 chromedriver.exe 设置环境变量
	driver.get(url)
	return driver