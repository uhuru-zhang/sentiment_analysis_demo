# 数据分析模块

## 1. 热度

### 1.1 事件的总热度

一个事件的热度$\rm Heat$定义如下：
$$
{\rm Heat}(e)=\sum_{与此事件相关的评论c}点赞数(c)+2
$$
**API如下：**

url: `{host}/algorithm/heat/{keyword}/`

返回：

- keyword
- heat_num

### 1.2 事件某天的评论数

用一个事件某天的评论数表示此事件这天的热度。

**API如下：**

url: `{host}/algorithm/heat_by_day/{keyword}/{day}`

注意：day的格式为`\d{4}-\d{2}-\d{2}`，如`2018-09-11`

返回：

- keyword
- comment_num
- day

## 2 热词

热词即事件的关键词，这里使用提供两种获取关键词的方法：TFIDF权重和TextRank方法，其中后者慢许多。

**API如下：**

url: `{host}/algorithm/hot_words/{keyword}/`

args:

- method: TDIDF或TextRank
- topk: 默认为10

返回：

- keyword: 事件的关键词
- count: 热词的数量
- hot_words: 列表，每一项的格式为 (word, weight)