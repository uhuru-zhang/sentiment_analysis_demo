"""
爬取今日头条的新闻及评论，实现基本的轮子

暂不支持今日头条站外新闻

实现的函数
1. get_news_addr(keyword="砍人者反被砍",limit=100)
2. get_news_content(addr)
3. get_comments(addr,limit=1000)
"""

import re
import json
import time
from bs4 import BeautifulSoup

try:
    from .lib import simple_download, download_use_chromedriver
except:
    from lib import simple_download, download_use_chromedriver


INF = 1e9

def get_news_addr(keyword="砍人者反被砍", limit=100, min_comment_count=0, count_once=5):
    """
    功能
     - 根据关键词获取头条中的新闻地址，默认获取超过100篇新闻地址后停止。

    输出
     - [(title,group_id,item_id,comment_count,datetime,tag),...]

    需要注意的是，会出现以下问题：
     - 会找到一些不相关的新闻。这个问题通过精确检索等方法进行改善。
     - 会找到一些内容重复的新闻。这个问题有两个考虑角度：
       (1) 如仅参考评论意见，则没有必要考虑二者差异，
       (2) 使用一些文本处理方法去重，合并评论。
     - 会返回站外新闻。
    """
    url = 'https://www.toutiao.com/search_content/'
    count = min(count_once,limit) # 一次获取多少新闻
    args = {
        'keyword': keyword,
        'offset': 0,  # 从第0条新闻开始
        'count': count,  # 一次爬去20条新闻
        'format': 'json',
        'from': 'search_tab',
        'cur_tab': 1,
        'autoload': 'true'
    }
    has_more = 1  # 还有更多新闻
    news_addr = []
    comment_num = 0

    while has_more == 1 and len(news_addr) < limit:
        wbdata = simple_download(url, args)
        data = json.loads(wbdata)
        has_more = data['has_more']
        many_news = data['data']

        for news in many_news:
            if 'cell_type' in news:
                continue
            has_gallery = news['has_gallery']
            if has_gallery:
                continue
            
            comment_count = int(news['comment_count']) # 通过局部观察，group_id 和 item_id 是一样的
            if comment_count <= min_comment_count:
                continue
            comment_num += comment_count
            tuple_ = (news['title'], news['group_id'], 
                news['item_id'],comment_count,
                news['datetime'],news['tag'])
            news_addr.append(tuple_)
            
        args['offset'] += count

    return news_addr,comment_num


def _write_addr(dir_, addrs):
    """将地址列表内写入到指定路径中"""
    with open(dir_, 'w', encoding='utf-8') as file_out:
        file_out.writelines([str(addr) + '\n' for addr in addrs])


def get_time_from_str(str_):
    """
    s 例如 原创 水木然 2018-08-30 23:11:30
    """
    str_time = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',str_)
    if not str_time:
        return -1
    str_time = str_time.group()
    struct_time = time.strptime(str_time,'%Y-%m-%d %H:%M:%S')
    return int(time.mktime(struct_time))


def get_news_content(addr):
    """
    根据地址爬取新闻正文
    输出字段：source_url,title,document,publication_at,tags,category
    """
    _,group_id,_,comment_count,datetime,category = addr
    source_url = 'https://www.toutiao.com/group/' + group_id
    driver = download_use_chromedriver(source_url)
    html = driver.page_source
    current_url = driver.current_url
    driver.quit()

    # print (current_url)
    if 'https://www.toutiao.com' not in current_url:  # 链接位于头条站外
        return -1

    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1', class_='article-title').text

    document = soup.find('div', class_='article-content').text

    # publication_at = soup.find('div', class_='article-sub').text
    publication_at = get_time_from_str(datetime)

    return source_url, title, document, publication_at, category


def get_comments(addr, limit=1000, count_once=20):
    """
    功能：爬取文章下面的评论，暂不考虑评论下的回复
    输出举例：[('支持。骑车哥无罪释放。大家都顶起来。', 283, 1535646388),...]
    """
    limit = int(limit)
    if limit == -1:
        limit = INF

    count = min(count_once,limit)
    _, group_id, item_id = addr[:3]
    url = 'https://ic.snssdk.com/article/v3/tab_comments/'
    args = {
        'group_id': group_id,
        'item_id': item_id,
        'offset': 0,  # 从第0条新闻开始
        'count': count,  # 一次爬去20条新闻
        'device_platform':'android'
    }

    has_more = True  # 还有更多新闻
    comments = []

    while has_more == True and len(comments) < limit:

        wbdata = simple_download(url, args)

        wbdata = json.loads(wbdata)
        has_more = wbdata['has_more']
        data = wbdata['data']

        for comment in data:
            comment = comment['comment']
            content = comment['text']
            upvote  = comment['digg_count']
            publication_at = comment['create_time']
            comments.append((content, upvote, publication_at))
        
        # print(len(comments))
        args['offset'] += count
        
    return comments


if __name__ == '__main__':
    addr2 = ('知情人眼中的昆山“反杀砍人者”于海明：三个孩子的父亲 “人很和善”', '6595411268977295886', '6595411268977295886', 68965, '2018-08-30 15:24:10', 'news_society')

    ## 功能1：根据关键词，爬取新闻地址 6595411268977295886
    # addrs,comment_num = get_news_addr(keyword="砍人者被反杀",limit=100, min_comment_count=10,count_once=5)

    ## 功能2：根据地址，获取文章正文
    # r = get_news_content(addr2)
    # print (r)

    # 功能3：根据地址，获取评论
    r = get_comments(addr2,count_once=40,limit=-1)
    print (len(r)) # 28078
    
