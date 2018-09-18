import json 

from django.shortcuts import render
from django.http import HttpResponse

from sentiment_analysis.dao import article as article_sql
from .crawler import TOUTIAO


def get_news_addr(request,keyword='北马 咸猪手',count=20):
	"""
	args:
	 keyword: 新闻的关键词
	 count: 大致数目，一般误差在5以内
	"""
	crawler = TOUTIAO(article_sql)
	addrs = crawler.get_news_addr(keyword, int(count))
	data = {
		'keyword': keyword,
		'count':len(addrs),
		'format':'title,group_id,item_id',
		'news_addrs':addrs,
	}
	json_ = json.dumps(data,ensure_ascii=False)
	crawler.save_keyword_and_addrs(keyword,addrs)
	return HttpResponse(json_,content_type="application/json") 
	

def toutiao_article(request,keyword_id,addr):
	crawler = TOUTIAO(article_sql)
	article  = crawler.get_news_content(addr)
	comments = crawler.get_comments(addr)
	crawler.save_article(article,keyword_id)
	crawler.save_comments(comments,article_id)
	return HttpResponse(addrs,keyword_id)
	
def test(request,keyword="北马咸猪手"):
	data = {
		'keyword':keyword,
		'id': 123 }
	json_ = json.dumps(data,ensure_ascii=False)
	return HttpResponse(json_,content_type="application/json")