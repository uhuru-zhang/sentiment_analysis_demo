import time
import json

from django.http import HttpResponse
from sentiment_analysis.dao import article as article_sql


def event_heat(request,keyword):
	sql = 'select review.series_id,review.content,review.upvote_num \
		   from keyword,review \
		   where keyword.content="{keyword}" and \
				 keyword.object_id=review.object_id;'.format(keyword=keyword)
	comments = article_sql.execute_sql(sql)
	heat_num = 0
	for comment in comments:
		heat_num += comment.upvote_num + 2

	data = {
		'keyword': keyword,
		'heat_num':heat_num,
	}
	json_ = json.dumps(data,ensure_ascii=False)
	return HttpResponse(json_,content_type="application/json")


def heat_by_day(request,keyword,day):
	sql = 'select 1 as series_id,\
		   count(*) as comment_count\
		   from keyword,review \
		   where keyword.content="{keyword}" and \
				 keyword.object_id=review.object_id and\
				 FROM_UNIXTIME(review.publication_at,\'%%Y-%%m-%%d\')="{day}";'.format(
				 	keyword=keyword,
				 	day=day)
	comment = article_sql.execute_sql(sql)[0]
	# print (1,comment[0].count)
	
	data = {
		'keyword' : keyword,
		'comment_num': comment.comment_count,
		'day':day
	}
	json_ = json.dumps(data,ensure_ascii=False)
	return HttpResponse(json_,content_type="application/json")
