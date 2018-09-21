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

- method: TDIDF或TextRank，默认为TDIDF
- topk: 默认为10
- source: 用于获取关键词的文本，取值是comment、article、all，默认值的all

返回：

- keyword: 事件的关键词
- count: 热词的数量
- hot_words: 列表，每一项的格式为 (word, weight)

## 3. 事件情感

通过来衡量事件新闻下评论的情感，进而估计事件对应的情感。具体来说，对于评论集合$C$，它整体的情感属于类别$c$的概率为
$$
p(w|C)=\frac{\sum_{c\in C} p(w|c)*{\rm confidence}(w|c)}{\sum_{c\in C}{\rm confidence}(w|c)}
$$
其中，$p(w|c)$为评论$c$的情感类别为$w$的概率，${\rm confidence}(w|c)$为评论$c$的情感类别为$w$的置信度。

**API如下：**

url: `{host}/algorithm/polarity/{keyword}/`

args:

- method: 情感分析的引擎，可选值 Baidu（默认值）、Boson、SELF（尚未实现）
- comment_num: 默认值为None表示全部，速度较慢，建议值30

返回：

- keyword
- engine: 情感分析的引擎
- comment_num
- polarity: 极性，0~1