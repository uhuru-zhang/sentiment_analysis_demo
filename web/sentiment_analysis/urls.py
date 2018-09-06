from django.contrib import admin
from django.urls import path, include

from .views import test_save, query_article, crawler

urlpatterns = [
    path("test_save", test_save),
    path("articles", query_article),
    path("crawler", crawler)
]
