from django.conf.urls import url
from .views import (
    AuthorList,
    AuthorDetails,
    AuthorDelete,
    AuthorUpdate,
    AuthorCreate
)
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'Authors'

urlpatterns = [
    url(r'^$', AuthorList.as_view(), name="author-list"),
    url(r'^(?P<pk>\d+)/$', AuthorDetails.as_view(), name="author-details"),
    url(r'^(?P<pk>\d+)/edit/$', AuthorUpdate.as_view(), name="author-update"),
    url(r'^(?P<pk>\d+)/delete/$', AuthorDelete.as_view(), name="author-delete"),
    url(r'^add/$', AuthorCreate.as_view(), name="author-create"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
