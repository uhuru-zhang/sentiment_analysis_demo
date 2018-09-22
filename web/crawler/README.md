# 数据获取模块

## 1 今日头条爬虫

**API如下：**

url: `{host}/crawler/main/{keyword}/{new_count}` 

注意：new_count 表示待爬取的新闻数量，但实际获取的文章数量40%左右。

args：

- thread_num: 最大线程数，实际只能利用大约 thread_num-20
- comment_num: 最大评论数，-1表示无限制

返回：

- keyword
- count: 地址数目
- format: ‘title,group_id,item_id,commet_count,datatime,tag’
- new_addrs: list