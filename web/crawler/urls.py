from django.urls import path, include
# from .views import test as views_test
from . import views
from django.conf.urls import url



urlpatterns = [
    # 例如 crawler/_get_news_addr/北马 咸猪手/10
    url(r'_get_news_addr/(?P<keyword>.*)/(?P<count>\d*)$',views.get_news_addr),
    # 例如 crawler/_get_news_content/北马 咸猪手?group_id=6601999400229143054&item_id=6601999400229143054$comment_num=1000
    url(r'_get_news_content/(?P<keyword>.*)$',views.get_news_content),
    # 例如 crawler/main/北马 咸猪手
    url(r'main/(?P<keyword>.*)/(?P<news_count>\d*)$',views.crawler_main),
]