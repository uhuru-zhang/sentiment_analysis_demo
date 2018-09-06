from ..models import Article
from ..dao import article as article_dao


def query_article(filters):
    return article_dao.query_articles(filters)
