from django.conf.urls import url
from .views import cached_views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'Recommend'

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', cached_views, name="Recommend-list"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
