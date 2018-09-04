from django.db import models


class BaseMeta(object):
    app_label = "sentiment_analysis"


class Article(models.Model):
    series_id = models.AutoField(primary_key=True)  # 序列ID
    title = models.TextField(default="")  # 文章标题
    document = models.TextField(default="")  # 文章内容
    publication_at = models.IntegerField(null=True)  # 发布时间
    category = models.IntegerField(null=True)  # 所属种类
    source_url = models.CharField(max_length=2 ** 10, null=True)  # 来源 URL
    source_type = models.IntegerField(default=-1)  # 来源种类 贴吧、天涯
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    extra = models.TextField(null=True)

    class Meta(BaseMeta):
        db_table = "article"


class PostBar(models.Model):
    series_id = models.AutoField(primary_key=True)
    theme_id = models.IntegerField()  # 主题 ID
    floor_id = models.IntegerField()  # 楼 ID
    title = models.TextField(default="")
    content = models.TextField(default="")
    source_url = models.CharField(max_length=2 ** 10, null=True)
    publication_at = models.IntegerField(null=True)
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    extra = models.TextField(null=True)

    class Meta(BaseMeta):
        db_table = "post_bar"
        indexes = [
            models.Index(fields=["theme_id", "floor_id"], name="theme_floor_index")
        ]


class Review(models.Model):
    series_id = models.AutoField(primary_key=True)
    object_type = models.IntegerField()  # 评论种类 0: Article 1: PostBar
    object_id = models.IntegerField()  # 内容ID
    content = models.TextField(default="")
    upvote_num = models.IntegerField(null=True)  # 点赞数
    publication_at = models.IntegerField(null=True)
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    extra = models.TextField(null=True)

    class Meta(BaseMeta):
        db_table = "review"
        indexes = [
            models.Index(fields=["object_type", "object_id"], name="object_type_id_index")
        ]
