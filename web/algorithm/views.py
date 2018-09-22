import time
import json

from django.http import HttpResponse

from sentiment_analysis.dao import article as article_sql

from .analysis.keyword_extract import keyword_by_TFIDF,keyword_by_textRank
from .analysis.polarity_analysis import Baidu_NLP,Boson_NLP
from .analysis.load_data import load_articles_by_keyword,\
								load_comments_by_keyword,\
								count_comments_by_day



def json_response(data):
	json_ = json.dumps(data,ensure_ascii=False)
	return HttpResponse(json_,content_type="application/json")


def event_heat(request,keyword):
	comments = load_comments_by_keyword(article_sql,keyword)
	heat_num = 0
	for comment in comments:
		heat_num += comment.upvote_num + 2

	data = {
		'keyword': keyword,
		'heat_num':heat_num,
	}
	return json_response(data)


def heat_by_day(request,keyword,day):
	comment_num = count_comments_by_day(keyword,day)
	
	data = {
		'keyword' : keyword,
		'comment_num': comment_num,
		'day':day
	}
	return json_response(data)


def keywords_from_comment(request,keyword):
	#===============加载参数===================
	method = request.GET.get('method') # TFIDF、TextRank
	if method is None:
		method = 'TFIDF'

	topK = request.GET.get('topK')
	if topK is None:
		topK = 10
	topK = int(topK)

	source = request.GET.get('source')
	if source is None:
		source = 'all'
	#================加载数据===================
	if source == 'comments':
		comments = load_comments_by_keyword(article_sql,keyword)
		text_list = [comment.content for comment in comments]

	elif source == 'article':
		articles = load_articles_by_keyword(article_sql,keyword)
		text_list = [article.document for article in articles]

	elif source == 'all':
		comments = load_comments_by_keyword(article_sql,keyword)
		articles = load_articles_by_keyword(article_sql,keyword)
		text_list = [comment.content for comment in comments] + [article.document for article in articles]
	else:
		raise ValueError("Unknown method type!")

	text = '\n'.join(text_list)
	#================数据分析===================
	if method == 'TFIDF':
		keywords = keyword_by_TFIDF(text,topK)

	elif method == 'TextRank':
		keywords = keyword_by_textRank(text,topK)

	else:
		raise ValueError("Unknown method type!")
	#================返回结果===================
	keywords = list(keywords)
	data = {
		'keyword' : keyword,
		'count': topK,
		'hot_words': keywords,
	}
	return json_response(data)


def polarity_of_the_event(request,keyword):
	method = request.GET.get('method') # Baidu、Boson、SELF
	comment_num = request.GET.get('comment_num') # Baidu、Boson、SELF
	if method is None:
		method = 'Baidu'
	if comment_num is not None:
		comment_num = int(comment_num)
	#================加载数据===================
	comments = load_comments_by_keyword(article_sql,keyword)
	text_list = [comment.content for comment in comments[:comment_num]]
	#================数据分析===================
	if method == 'Boson':
		nlp_engine = Boson_NLP()
	elif method == 'Baidu':
		nlp_engine = Baidu_NLP()
	elif method == 'SELF':
		return json_response({'message' : '尚未实现'})
	else:
		raise ValueError("Unknown method type!")
	polarity = nlp_engine.polarity_of_list(text_list)
	#================返回结果===================
	data = {
		'keyword': keyword,
		'engine':  method,
		'comment_num': len(text_list),
		'polarity': polarity
	}
	return json_response(data)


def polarity_of_text(request):
	text   = request.GET.get('text')
	method = request.GET.get('method')
	if text is None:
		return json_response({'message' : '文本为空'})
	if method  is None:
		method = 'Baidu'
	#================数据分析===================
	if method == 'Boson':
		nlp_engine = Boson_NLP()
	elif method == 'Baidu':
		nlp_engine = Baidu_NLP()
	elif method == 'SELF':
		return json_response({'message' : '尚未实现'})
	else:
		raise ValueError("Unknown method type!")
	polarity = nlp_engine.polarity_of_text(text)
	#================返回结果===================
	data = {
		'text': text,
		'engine':  method,
		'polarity': polarity
	}
	return json_response(data)

