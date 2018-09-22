"""
BeautifulSoup
selenium 
 - chromedriver.exe
"""

import sys
import time
# import threading

from . import toutiao
from .lib import General_Thread



class TOUTIAO:

	def __init__(self,article_sql):
		self.article_sql = article_sql

	def get_news_addr(self, keyword, max_news_num):
		return toutiao.get_news_addr(keyword, max_news_num)

	def get_news_content(self, addr):
		return toutiao.get_news_content(addr)

	def get_comments(self, addr, limit):
		return toutiao.get_comments(addr,count_once=50,limit=limit)

	def save_keyword_and_addrs(self,keyword,addrs):
		for addr in addrs:
			self.article_sql.save_keyword(
				object_type=-1, object_id=-1,
				content=keyword, article_url=addr, extra="TOUTIAO")
    
	def save_article(self,article,keyword):
		source_url, title, document, publication_at, category = article
		
		id_, type_ = self.article_sql.save_article(title=title, document=document,
					publication_at=publication_at, category=category,
					source_url=source_url, source_type=0, extra="")
		self.article_sql.save_keyword(
			content=keyword, object_type=type_, object_id=id_)
		return type_,id_

	def save_comments(self,comments,type_,id_):
		for comment in comments:
			content, upvote, publication_at,_ = comment
			self.article_sql.save_review(object_type=type_, 
				object_id=id_, content=content, upvote_num=upvote, 
				publication_at=publication_at, extra="")


if __name__ == "__main__":
	crawler = TOUTIAO(article_sql)
	crawler.crawl_and_save('砍人者反被砍', 4)
