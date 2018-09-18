from django.urls import path, include
# from .views import test as views_test
from . import views
from django.conf.urls import url



urlpatterns = [
    # url(r'toutiao/$','crawler.views.index'),)
    # path(r"toutiao", index),
    url(r'test/(?P<keyword>.*)$',views.test),
    url(r'get_news_addr/(?P<keyword>.*)/(?P<count>\d*)$',views.get_news_addr)
]