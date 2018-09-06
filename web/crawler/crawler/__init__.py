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

# except:
	 # from web.sentiment_analysis.dao import article as article_sql


# class Gennral_thread(threading.Thread):

# 	def __init__(self, func, data, count=0):
# 		print("in Gennral_thread init!")
# 		super(Gennral_thread, self).__init__()
# 		self.func = func
# 		self.data = data
# 		self.count = count

# 	def run(self):
# 		print("in Gennral_thread run!")
# 		self.count += 1
# 		if self.count > 3:
# 			print('$')

# 		# try:
# 		self.func(*self.data)
# 	# except:
# 	# 	time.sleep(2)
# 	# 	print ('*')
# 	# 	Gennral_thread(self.func,self.data,self.count+1)


# def wait_for_thread(wait_time=180):
# 	t = 0
# 	while threading.activeCount() > 1:
# 		time.sleep(1)
# 		t += 1
# 		if t > 180:
# 			return


class TOUTIAO:

	def __init__(self,article_sql):
		self.article_sql = article_sql

	def _get_news_addr(self, keyword, max_news_num):
		return toutiao.get_news_addr(keyword, max_news_num)

	def _get_news_content(self, addr):
		return toutiao.get_news_content(addr)

	def _get_comments(self, addr):
		return toutiao.get_comments(addr)

	def crawl_and_save_single(self, addr):
		tuple_ = self._get_news_content(addr)
		if tuple_ == -1:  # 失败
			print('@')
			return
		source_url, title, document, publication_at, tags, category = tuple_
        
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

	def crawl_and_save(self, keyword, max_news_num, thread_num=10):
		addrs = self._get_news_addr(keyword, max_news_num)

		for num, addr in enumerate(addrs[2:]):
			print(num, addr)
			self.crawl_and_save_single(addr)  

	def crawl_and_save_with_many_thread(self, keyword, max_news_num=100, thread_num=10):
		def run():
			self.crawl_and_save(keyword, max_news_num)


if __name__ == "__main__":
	crawler = TOUTIAO(article_sql)
	crawler.crawl_and_save('砍人者反被砍', 4)
