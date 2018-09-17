from django.urls import path, include
from .views import index


urlpatterns = [
    # url(r'toutiao/$','crawler.views.index'),)
    path(r"toutiao", index),
]