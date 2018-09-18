"""
BeautifulSoup
selenium 
 - chromedriver.exe
"""

import sys
import time
# import threading

try:
	import toutiao
except:
	from . import toutiao



class TOUTIAO:

	def __init__(self,article_sql):
		self.article_sql = article_sql

	def get_news_addr(self, keyword, max_news_num):
		return toutiao.get_news_addr(keyword, max_news_num)

	def get_news_content(self, addr):
		return toutiao.get_news_content(addr)

	def get_comments(self, addr):
		return toutiao.get_comments(addr)

	def save_keyword_and_addrs(self,keyword,addrs):
		# unfinished
		for addr in addrs:
			self.article_sql.save_keyword(
				object_type=-1, object_id=-1,
				content=keyword, article_url=addr[1], extra="TOUTIAO")
    
	def save_article(self,article,keyword_id):
		source_url, title, document, publication_at, tags, category = article
		extra = 'tags: %s' % tags
		id_, type_ = self.article_sql.save_article(title=title, document="",
					publication_at=publication_at, category=category,
					source_url=source_url, source_type=0, extra=extra)
		self.article_sql.update_keyword_object_id(
			series_id=keyword_id,
			object_type=type_,object_id=id_)

	def save_comments(self,comments):
		for comment in comments:
			content, upvote, publication_at = comment
			self.article_sql.save_review(object_type=type_, object_id=id_,
									 content=content, upvote_num=upvote, publication_at=publication_at, extra="")

		

	def crawl_and_save_single(self, addr):
		tuple_ = self.get_news_content(addr)
		if tuple_ == -1:  # 失败
			print('@')
			return
		
        
		extra = 'tags: %s' % tags
		id_, type_ = self.article_sql.save_article(title=title, document="",
											   publication_at=publication_at, category=category,
											   source_url=source_url, source_type=0, extra=extra)
		
		comments = self._get_comments(addr)
		for comment in comments:
			# print(comment)
			content, upvote, publication_at = comment
			self.article_sql.save_review(object_type=type_, object_id=id_,
									 content=content, upvote_num=upvote, publication_at=publication_at, extra="")

	def crawl_and_save(self, keyword, max_news_num):
		addrs = self.get_news_addr(keyword, max_news_num)

		for num, addr in enumerate(addrs):
			print(num, addr)
			self.crawl_and_save_single(addr)


if __name__ == "__main__":
	crawler = TOUTIAO(article_sql)
	crawler.crawl_and_save('砍人者反被砍', 4)
