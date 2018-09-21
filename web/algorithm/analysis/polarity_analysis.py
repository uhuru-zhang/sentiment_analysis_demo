import re

from aip import AipNlp
from bosonnlp import BosonNLP



def drop_ungbk(text):
	"""去除gbk不能编码的字符"""
	# https://blog.csdn.net/PoPoQQQ/article/details/77960206?utm_source=copy 
	# pattern = '\\\\U[a-f0-9]{8}|\\\\u[a-f0-9]{4}|\\\\x[a-f0-9]{2}'
	# return re.sub(pattern, '', text, count=0, flags=0)
	return text.encode('gbk',errors='ignore').decode('gbk')


class Baidu_NLP:

	def __init__(self,
		APP_ID = '14258345',
		API_KEY = 'cLOxZEYdKYdOwN2j5kXBLnSW',
		SECRET_KEY = 'wxNjQw0GDTmR5xIYOZ5qUc5gWjGOmwt5'):

		self.client = AipNlp(APP_ID,API_KEY,SECRET_KEY)

	def polarity_of_text(self,text):
		"""
		返回值：
		 - 正面指数，0到1之间
		 - 置信度
		"""
		text = drop_ungbk(text)
		if not text:
			return 0.5,0
		response = self.client.sentimentClassify(text)
		if 'error_code' in response:
			return 0.5,0
		sentiment = response['items'][0]
		return sentiment['positive_prob'],sentiment['confidence']

	def polarity_of_list(self,lst):
		positive_rate = 0
		confidence = 0
		for text in lst:
			pp,co = self.polarity_of_text(text)
			positive_rate += pp*co 
			confidence += co
		return positive_rate/confidence


class Boson_NLP:

	def __init__(self,API_TOKEN='ADdt3aLr.27579.d0xt4IOfHR96'):
		self.nlp = BosonNLP(API_TOKEN)

	def polarity_of_text(self,text):
		"""
		返回值：
		 - 正面指数，0到1之间
		 - 置信度
		"""
		return self.nlp.sentiment(text,model='news')[0][0],1

	def polarity_of_list(self,lst):
		"""
		返回值：正面指数，0到1之间
		"""
		len_ = len(lst)
		results = self.nlp.sentiment(lst,model='news')
		positive_rate = 0
		for i in range(len_):
			positive_rate += results[i][0]
		return positive_rate/len_


if __name__=='__main__':
	c = ['家产充公，重判，正我国威',
		'必须封杀这类人，罚他个倾家荡产',
		'洗钱抓起来，判刑二十年。',
		'这人真坏。','']

	bnlp = Baidu_NLP()
	result = bnlp.polarity_of_list(c)
	print (result)