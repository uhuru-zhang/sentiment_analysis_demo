"""
参考： https://www.jianshu.com/p/cf383fd471bb
"""


def load_comments_by_keyword(article_sql,keyword):
	sql = 'select 1 as series_id,review.content \
		   from keyword,review \
		   where keyword.content="{keyword}" and \
				 keyword.object_id=review.object_id;'.format(keyword=keyword)
	comments = article_sql.execute_sql(sql)
	return comments


def load_articles_by_keyword(article_sql,keyword):
	sql = 'select 1 as series_id,article.document \
		   from keyword,article \
		   where keyword.content="{keyword}" and \
				 keyword.object_id=article.series_id;'.format(keyword=keyword)
	articles = article_sql.execute_sql(sql)
	return articles

