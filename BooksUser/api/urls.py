from django.conf.urls import url
from .views import (
    BookUserList,
    book_user,
    BookUserDelete,
    BookUserUpdate,
    BookUserCreate
)
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'BookUser'

urlpatterns = [
    url(r'^$', BookUserList.as_view(), name="book_user-list"),
    url(r'^add/$', BookUserCreate.as_view(), name="book_user-create"),
    url(r'^(?P<book>\d+)/(?P<user>\d+)/$', book_user, name="book_user-details"),
    url(r'^(?P<pk>\d+)/edit/$', BookUserUpdate.as_view(), name="book_user-update"),
    url(r'^(?P<pk>\d+)/delete/$', BookUserDelete.as_view(), name="book_user-delete")
]
urlpatterns = format_suffix_patterns(urlpatterns)
