from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from .views import (
    MessageDetails,
    MessageDelete,
    MessageUpdate,
    MessageAll
)

app_name = 'Categories'

urlpatterns = [
    url(r'^$', MessageAll.as_view(), name="messages-list"),
    url(r'^(?P<pk>\d+)/$', MessageDetails.as_view(), name="messages-details"),
    url(r'^(?P<pk>\d+)/edit/$', MessageUpdate.as_view(), name="messages-update"),
    url(r'^(?P<pk>\d+)/delete/$', MessageDelete.as_view(), name="messages-delete")
]
urlpatterns = format_suffix_patterns(urlpatterns)
