"""
参考： https://www.jianshu.com/p/cf383fd471bb
"""


def load_comments_by_keyword(article_sql,keyword):
	sql = 'select 1 as series_id,review.content,review.upvote_num \
		   from keyword,review \
		   where keyword.content="{keyword}" and \
				 keyword.object_id=review.object_id;'.format(keyword=keyword)
	comments = article_sql.execute_sql(sql)
	return comments


def count_comments_by_day(article_sql,keyword,day):
	r'''
	day的格式 \d{4}-\d{2}-\d{2}
	'''
	sql = 'select 1 as series_id,\
		   count(*) as comment_count\
		   from keyword,review \
		   where keyword.content="{keyword}" and \
				 keyword.object_id=review.object_id and\
				 FROM_UNIXTIME(review.publication_at,\'%%Y-%%m-%%d\')="{day}";'.format(
				 	keyword=keyword,
				 	day=day)

	comment = article_sql.execute_sql(sql)[0]
	return comment.count


def load_articles_by_keyword(article_sql,keyword):
	sql = 'select 1 as series_id,article.document \
		   from keyword,article \
		   where keyword.content="{keyword}" and \
				 keyword.object_id=article.series_id;'.format(keyword=keyword)
	articles = article_sql.execute_sql(sql)
	return articles


