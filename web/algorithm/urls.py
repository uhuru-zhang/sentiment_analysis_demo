from . import views
from django.conf.urls import url



urlpatterns = [
    # 例如 algorithm/heat/北马 咸猪手
    url(r'heat/(?P<keyword>.*)/$',views.event_heat),
    # 例如 algorithm/heat_by_day/北马 咸猪手/2018-09-20
    url(r'heat_by_day/(?P<keyword>.*)/(?P<day>\d{4}-\d{2}-\d{2})$',views.heat_by_day),
    # 例如 algorithm/hot_words/北马 咸猪手/
    url(r'hot_words/(?P<keyword>.*)/$',views.keywords_from_comment),
    # 例如 algorithm/polarity/北马 咸猪手/
    url(r'polarity/(?P<keyword>.*)/$',views.polarity_of_the_event)
]