from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from .views import (
    FollowList,
    follow,
    follow_delete,
    FollowCreate,
)

app_name = 'Followers'

urlpatterns = [
    url(r'^$', FollowList.as_view(), name="Follow-list"),
    url(r'^(?P<flr>\d+)/(?P<flg>\d+)/$', follow, name="Follow-details"),
    url(r'^(?P<flr>\d+)/(?P<flg>\d+)/delete/$', follow_delete, name="Follow-delete"),
    url(r'^add/$', FollowCreate.as_view(), name="Follow-create")
]
urlpatterns = format_suffix_patterns(urlpatterns)
