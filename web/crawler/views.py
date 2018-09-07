from django.shortcuts import render
from django.http import HttpResponse

from sentiment_analysis.dao import article as article_sql
from .crawler import TOUTIAO

def index(request):
	crawler = TOUTIAO(article_sql)
	crawler.crawl_and_save('砍人者反被砍', 10)
	return HttpResponse(1)