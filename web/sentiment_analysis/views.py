import json
from time import time

from django.http import HttpResponse
# Create your views here.
from django.views.decorators.http import require_POST

# from web.crawler.crawler import TOUTIAO
from .controller import article as article_controller
from .dao import article as article_dao


def test_save(request):


    for i in range(100):
        a, _ = article_dao.save_article(title="test_title_{}".format(i), document="test_document_{}".format(i),
                                        publication_at=time() - 60 * 60 * 24 * i, category="{}".format(i % 3),
                                    source_url="test_source_url", source_type=100)
        # print(article_dao.save_article(title="test_title", document="test_document", publication_at=100, category=100,
        #                            source_url="test_source_url", source_type=100))
        # print(article_dao.save_review(object_type=10, object_id=a, content="content", upvote_num=10, publication_at=10))
    return HttpResponse("Success saved {} rows".format(100))


@require_POST
def query_article(request):
    data = article_controller.query_article(json.loads(request.body))
    print(data)
    return HttpResponse(json.dumps(data), content_type="application/json")


# def crawler(request):
#     crawler = TOUTIAO()
#     crawler.crawl_and_save('砍人者反被砍', 10, thread_num=1)
#     return HttpResponse("Success !")
