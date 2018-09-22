"""
参考： https://www.jianshu.com/p/cf383fd471bb
"""
import jieba.analyse as jieba_al 



def keyword_by_TFIDF(text,topK=10):
	"""
	text 可以是列表或者字符串
	"""
	return jieba_al.extract_tags(text,withWeight=True,topK=topK)
	

def keyword_by_textRank(text,topK=10):
	"""
	text 可以是列表或者字符串
	"""
	return jieba_al.textrank(text,withWeight=True,topK=topK)


if __name__ == '__main__':
	str_ = "你还摸肚子，陌生人的手我都没摸过！这样不对，中国人有一句古话说的好。不以。善小而不为。不以。恶小而为之。我觉得如果是击掌就没问题，摸肚子就不对了，我也是佩服这位老哥。跑马拉松。累得要死。还有时间。玩这个。你的脑袋里一天想什么？猪。"
	print (keyword_by_textRank(str_))




