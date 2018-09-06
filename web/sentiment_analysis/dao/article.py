import time
import uuid

from ..const import object_type_dict
from ..models import Article, Review


def query_articles(filters, limit=(0, 100)):
    raw_query = """
        select series_id, title, publication_at, category, source_url, source_type
        from article 
        where publication_at between {publication_at}
          and source_type={source_type}
          limit {limit}
    """.format(
        publication_at=" and ".join(map(str, filters["publication_at"])),
        source_type=filters["source_type"] if "source_type" in filters else "source_type",
        limit=", ".join(map(str, filters.get("limit", limit)))
    )

    print(raw_query)
    return Article.objects.raw(raw_query=raw_query)


def save_article(title="", document="", publication_at=0, category=0, source_url="", source_type=0, extra=""):
    series_id = uuid.uuid1()

    Article(
        series_id=series_id,
        title=title,
        document=document,
        publication_at=publication_at,
        category=category,
        source_url=source_url,
        source_type=source_type,
        created_at=int(time.time()),
        updated_at=int(time.time()),
        extra=extra
    ).save()

    return series_id, object_type_dict["article"]


def save_review(object_type, object_id, content="", upvote_num=0, publication_at=0, extra=""):
    series_id = uuid.uuid1()

    Review(
        series_id=series_id,
        object_type=object_type,
        object_id=object_id,
        content=content,
        upvote_num=upvote_num,
        publication_at=publication_at,
        created_at=int(time.time()),
        updated_at=int(time.time()),
        extra=extra
    ).save()

    return series_id
