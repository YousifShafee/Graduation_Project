from django.conf.urls import url
from .views import (
    BookList,
    book_list,
    book_details,
    BookCreate,
    BookUpdate,
    BookDelete,
    books,
    index_list,
)
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'Books'

urlpatterns = [
    url(r'^$', BookList.as_view(), name="book-list"),
    url(r'^add/$', BookCreate.as_view(), name="book-create"),
    url(r'^(?P<pk>\d+)/$', book_details, name="book-details"),
    url(r'^(?P<pk>\d+)/edit/$', BookUpdate.as_view(), name="book-update"),
    url(r'^(?P<pk>\d+)/delete/$', BookDelete.as_view(), name="book-delete"),
    url(r'^index/(?P<pk>\d+)/$', books, name='index'),
    url(r'^(?P<var>[\w-]+)/$', index_list, name='recent & rate'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
