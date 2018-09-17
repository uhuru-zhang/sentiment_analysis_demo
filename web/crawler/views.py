from django.shortcuts import render
from django.http import HttpResponse

from sentiment_analysis.dao import article as article_sql
from .crawler import TOUTIAO


def toutiao_get_addr(request,keyword):
	crawler = TOUTIAO(article_sql)
	addrs,keyword_id = crawler.get_news_addr('北马 咸猪手', 1)
	crawler.save_addrs(addrs)
	return HttpResponse(addrs,keyword_id)
	

def toutiao_article(request,keyword_id,addr):
	crawler = TOUTIAO(article_sql)
	article  = crawler.get_news_content(addr)
	comments = crawler.get_comments(addr)
	crawler.save_article(article,keyword_id)
	crawler.save_comments(comments,article_id)
	return HttpResponse(addrs,keyword_id)
	