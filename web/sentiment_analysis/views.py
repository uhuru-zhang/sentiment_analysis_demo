import json

from django.http import HttpResponse
# Create your views here.
from django.views.decorators.http import require_POST

from .controller import article as article_controller
from .dao import article as article_dao


def test_save(request):
    article_dao.save_article(title="test_title", document="test_document", publication_at=100, category=100,
                             source_url="test_source_url", source_type=100)
    article_dao.save_review(object_type=10, object_id=10, content="content", upvote_num=10, publication_at=10)
    return HttpResponse("Success saved {} rows".format(1000))


@require_POST
def query_article(request):
    return HttpResponse(article_controller.query_article(json.loads(request.body)))
