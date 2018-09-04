"""
爬取今日头条的新闻
"""

import requests
import random
import json
from bs4 import BeautifulSoup
from selenium import webdriver



my_headers=["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
			"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
			'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
			'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
			'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
			'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ',  
			'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)']


def download_html(url,args={}):
	"""根据url，下载网页"""
	random_header = random.choice(my_headers)
	headers = {'User-Agent' : random_header}
	data = requests.get(url,headers=headers,params=args)
	data.encoding = 'utf-8'
	return data.text

def download_html2(url,args={}):
	driver = webdriver.Chrome('D:/Computer_software/chromedriver1.exe')
	driver.get(url)
	return driver


def get_news_addr(keyword="砍人者反被砍",limit=100):
	"""
	根据关键词获取头条中的新闻地址，默认获取超过100篇新闻地址后停止。
	需要注意的，会出现以下问题：
	 - 会找到一些不相关的新闻。这个问题通过精确检索等方法进行改善。
	 - 会找到一些内容重复的新闻。这个问题有两个考虑角度，
	   (1) 如仅参考评论意见，则没有必要考虑二者差异，(2) 使用一些文本处理方法去重，合并评论。
	"""
	url = 'https://www.toutiao.com/search_content/'
	args = {
		'keyword': keyword,
		'offset': 0,  # 从第0条新闻开始
		'count': 20,  # 一次爬去20条新闻
		'format': 'json',
		'from': 'search_tab',
		'cur_tab': 1,
		'autoload': 'true'
	}
	has_more = 1 # 还有更多新闻
	news_addr = []
	while has_more == 1 and len(news_addr)<limit:
		wbdata = requests.get(url,args).text
		data = json.loads(wbdata)
		has_more = data['has_more']
		many_news = data['data']
		for news in many_news:
			try:
				news_addr.append((news['title'],news['item_source_url']))
				# print(news_addr[-1])
			except: # 不知道会出什么错误
				pass
		args['offset'] += 20

	return news_addr


def get_news_content(addr):
	"""根据地址爬取新闻正文"""
	source_url = 'https://www.toutiao.com'+addr[1]
	driver = download_html2(source_url)
	html = driver.page_source
	driver.quit()
	# print (html)
	soup = BeautifulSoup(html,'html.parser')
	try:
		title = soup.find('h1',class_='article-title').text
		document = soup.find('div',class_='article-content').text
		publication_at = soup.find('div',class_='article-sub').text
		tags = soup.find('ul',class_='tag-list').text 
	except:
		return html
	return source_url,title,document,publication_at,tags
	
######################
"""
接下来需要做的是
1. 爬取评论
2. 爬取其他网站
3. 保存
"""
  



if __name__ == '__main__':
	# addrs = get_news_addr(keyword="砍人者反被砍",limit=100)
	# print (len(addrs))
	addr1 = ('别惹老实人！砍人甩飞刀，结果反被杀……', '/group/6594746535194395143/')
	addr2 = ('宝马男砍人反被砍死，千万不要把老实人逼上绝路！', '/group/6595531287157539336/')
	r = get_news_content(addr2)
	print (r)