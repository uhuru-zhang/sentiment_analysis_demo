import time
import json
import random
import requests
import threading

from django.shortcuts import render
from django.http import HttpResponse

from sentiment_analysis.dao import article as article_sql
from .crawler import TOUTIAO,General_Thread


def get_news_addr(request,keyword='北马 咸猪手',count=20):
	"""
	args:
	 keyword: 新闻的关键词
	 count: 大致数目，一般误差在5以内
	"""
	crawler = TOUTIAO(article_sql)
	addrs = crawler.get_news_addr(keyword, int(count))[0]
	# crawler.save_keyword_and_addrs(keyword,addrs)
	data = {
		'keyword': keyword,
		'count':len(addrs),
		'format':'title,group_id,item_id,commet_count,datatime,tag',
		'news_addrs':addrs,
	}
	json_ = json.dumps(data,ensure_ascii=False)
	return HttpResponse(json_,content_type="application/json") 
	

def get_news_content(request,keyword):
	"""
	args:
	 keyword: 新闻对应的关键词
	 addr: 新闻的的地址
	 comment_num: 评论的最大数目(不精确)
	"""
	group_id = request.GET.get('group_id')
	item_id  = request.GET.get('datetime')
	datetime = request.GET.get('datetime')
	category = request.GET.get('category')
	comment_num = request.GET.get('comment_num')
	comment_num = int(comment_num)

	addr = None,group_id,item_id,None,datetime,category

	crawler = TOUTIAO(article_sql)
	article  = crawler.get_news_content(addr)

	if article is -1:
		data = {'status': 'failure'}
		json_ = json.dumps(data,ensure_ascii=False)
		return HttpResponse(json_,content_type="application/json")

	comments  = crawler.get_comments(addr,comment_num)

	type_,id_ = crawler.save_article(article,keyword)
	crawler.save_comments(comments,type_,id_)

	data = {
		'status': 'success',
		'title' :  article[2],
		'comment_num': len(comments),
	}
	json_ = json.dumps(data,ensure_ascii=False)

	# print ('>>>',article[1],len(comments))

	return HttpResponse(json_,content_type="application/json")


def crawler_main(request,keyword,news_count=30):
	"""
	args:
	 keyword: 新闻关键词
	 news_count: 爬去的新闻数量（近似）
	 thread_num: 最大线程数量，包含了系统中的其他线程，
	 	故达不到这个数字，大概会少20多个，不应该超过120
	 comment_count: 最大评论数目
	"""
	thread_num = request.GET.get('thread_num')
	if thread_num is None:
		print (thread_num)
		thread_num = 50
	thread_num = int(thread_num)
	comment_num = request.GET.get('comment_num')
	if comment_num is None:
		comment_num = -1
	comment_num = int(comment_num)

	host = request.get_host()
	url_addr = 'http://{host}/crawler/_get_news_addr/{keyword}/{news_count}'.format(
		host=host,keyword=keyword,news_count=news_count)
	url_content = 'http://{host}/crawler/_get_news_content/{keyword}'

	wb_data = requests.get(url_addr)
	data = wb_data.json()
	news_addrs = data['news_addrs']

	for index,addr in enumerate(news_addrs):
		the_url = url_content.format(host=host,keyword=keyword)
		args = {
			'group_id': addr[1],
			'item_id':  addr[2],
			'datetime': addr[4],
			'category': addr[5],
			'comment_num': comment_num}
		while threading.activeCount()>min(thread_num,75):
			time.sleep(random.randint(1,5))
		General_Thread(requests.get,(the_url,args)).start()
		print (index,addr[0])

	return HttpResponse(wb_data,content_type="application/json")

