"""
爬取今日头条的新闻及评论，实现基本的轮子

暂不支持今日头条站外新闻

实现的函数
1. get_news_addr(keyword="砍人者反被砍",limit=100)
2. get_news_content(addr)
3. get_comments(addr,limit=1000)
"""

import json
from bs4 import BeautifulSoup

from .lib import simple_download, download_use_chromedriver


def get_news_addr(keyword="砍人者反被砍", limit=100):
    """
    功能
     - 根据关键词获取头条中的新闻地址，默认获取超过100篇新闻地址后停止。
    输出举例
     - [('宝马男砍人反被砍死，千万不要把老实人逼上绝路！', '6595531287157539336', '6595531287157539336'),...]
    需要注意的是，会出现以下问题：
     - 会找到一些不相关的新闻。这个问题通过精确检索等方法进行改善。
     - 会找到一些内容重复的新闻。这个问题有两个考虑角度：
       (1) 如仅参考评论意见，则没有必要考虑二者差异，
       (2) 使用一些文本处理方法去重，合并评论。
    """
    url = 'https://www.toutiao.com/search_content/'
    args = {
        'keyword': keyword,
        'offset': 0,  # 从第0条新闻开始
        'count': 20,  # 一次爬去20条新闻
        'format': 'json',
        'from': 'search_tab',
        'cur_tab': 1,
        'autoload': 'true'
    }
    has_more = 1  # 还有更多新闻
    news_addr = []
    while has_more == 1 and len(news_addr) < limit:
        wbdata = simple_download(url, args)
        data = json.loads(wbdata)
        has_more = data['has_more']
        many_news = data['data']
        for news in many_news:
            try:
                # 通过局部观察，group_id 和 item_id 是一样的
                news_addr.append((news['title'], news['group_id'], news['item_id']))
            # print(news_addr[-1])
            except:  # 不知道会出什么错误
                pass
        args['offset'] += 20

    return news_addr


def _write_addr(dir_, addrs):
    """将地址列表内写入到指定路径中"""
    with open(dir_, 'w', encoding='utf-8') as file_out:
        file_out.writelines([str(addr) + '\n' for addr in addrs])


def get_news_content(addr):
    """
    根据地址爬取新闻正文
    输出字段：source_url,title,document,publication_at,tags,category
    """

    source_url = 'https://www.toutiao.com/group/' + addr[1]
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
    publication_at = soup.find('div', class_='article-sub').text
    category = soup.find('div', class_="bui-left chinese-tag").text  # 首页\n/\n其他\n/\n正文
    category = category.split('\n')[2].strip()
    tags = soup.find('ul', class_='tag-list').text

    return source_url, title, document, publication_at, tags, category


def get_comments(addr, limit=1000):
    """
    功能：爬取文章下面的评论，暂不考虑评论下的回复
    输出举例：[('支持。骑车哥无罪释放。大家都顶起来。', 283, 1535646388),...]
    """
    _, group_id, item_id = addr
    url = 'https://www.toutiao.com/api/comment/list/'
    args = {
        'group_id': group_id,
        'item_id': item_id,
        'offset': 0,  # 从第0条新闻开始
        'count': 20,  # 一次爬去20条新闻
    }
    has_more = 1  # 还有更多新闻
    comments = []
    while has_more == 1 and len(comments) < limit:
        # wbdata = requests.get(url,args).text
        wbdata = simple_download(url, args)
        data = json.loads(wbdata)['data']
        has_more = data['has_more']
        many_comments = data['comments']
        limit = min(limit, data['total'])
        for comment in many_comments:
            content = comment['text']
            upvote = comment['digg_count']
            create_at = comment['create_time']
            comments.append((content, upvote, create_at))
            print(len(comments), comments[-1])
    return comments


if __name__ == '__main__':
    addr1 = ('别惹老实人！砍人甩飞刀，结果反被杀……', '6594746535194395143', '6594746535194395143')
    addr2 = ('宝马男砍人反被砍死，千万不要把老实人逼上绝路！', '6595531287157539336', '6595531287157539336')

    ## 功能1：根据关键词，爬取新闻地址
    # addrs = get_news_addr(keyword="砍人者反被砍",limit=100)
    # _write_addr('data/toutiao_addr.txt',addrs)

    ## 功能2：根据地址，获取文章正文
    # r = get_news_content(addr2)
    # print (r)

    # 功能2：根据地址，获取评论
    r = get_comments(addr2)
