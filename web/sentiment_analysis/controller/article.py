import datetime

from ..models import Article
from ..dao import article as article_dao


def query_article(filters):
    lines = article_dao.query_articles(filters)

    articles = {
        'rows': []
    }
    for article in lines:
        articles['rows'].append({
            "series_id": article.series_id,
            "title": article.title,
            "document": article.document,
            "publication_at": datetime.datetime.fromtimestamp(article.publication_at).strftime("%y-%m-%d %H:%M"),
            "category": article.category,
            "source_url": article.source_url
        })

    return articles
