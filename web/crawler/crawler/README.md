# 爬虫模块

这一部分的目标是根据关键词，批量爬取相关的新闻和评论。暂时只实现了对今日头条中新闻的爬取。

###1.1 今日头条爬虫

爬虫的入口地址为 [https://www.toutiao.com/search_content/](https://www.toutiao.com/search_content/)。数据爬取的流程如下：

- 首先，使用关键词搜索，批量获取文章地址。
- 然后，对于每一个文章地址爬取文章及评论。

需要注意的是，文章地址和评论内容需要通过API获得，而文章内容则需要爬虫模拟浏览器以获取。

**使用的工具**

- 数据下载：`requests`、`selenium`
- 网页解析：`BeautifulSoup`

###API简介、

**(1) 获取文章地址** 

URL：[https://www.toutiao.com/search_content/](https://www.toutiao.com/search_content/)

args:

- keyword: 关键词
- offset: 从第几条新闻开始
- count: 一次获取的新闻数目
- format: 数据返回格式，可选值 json
- cur_tab: 1-综合，2-视频，3-图集，4-用户，5-问答

返回数据格式

- has_more: 1
- data
  - list
    - title: 新闻标题
    - group_id: https://www.toutiao.com/group/+group_id 即为新闻的跳转地址，有可能跳转到站外去
    - article_url: 文章实际地址（非文章则无此字段），很大程度上是站外地址
    - abstract: 摘要
    - media_name: 新闻的发布媒体，如“聊城晚报”
    - datatime: 发布时间
    - tag: 如“news_entertainment”、"news_society"
    - comment_count: 评论数目
    - has_gallery: 是否为图集
    - cell_type: 
      - 文章 中无此字段
      - 50、66-微头条，如[https://www.toutiao.com/a1611807064233997/](https://www.toutiao.com/a1611807064233997/)
      - 37-问答：如[https://www.toutiao.com/a6594744260388454664/](https://www.toutiao.com/a6594744260388454664/)
      - 20-搜索推荐

注：对于一个关键词，共能返回200条。

**(2) 获取评论**

URL：https://www.toutiao.com/api/comment/list/

args：

- group_id（文章的id）
- item_id（一般与group_id一样）
- offset（从第几条新闻开始）
  - 																																																																																																																																																																																																																																																																																																																																																																																					count（获取的评论数目）