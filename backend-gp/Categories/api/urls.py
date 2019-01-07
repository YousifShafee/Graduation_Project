from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from .views import (
    CategoryCreate,
    CategoryList,
    CategoryDetails,
    CategoryDelete,
    CategoryUpdate,
)

app_name = 'Categories'

urlpatterns = [
    url(r'^$', CategoryList.as_view(), name="category-list"),
    url(r'^(?P<pk>\d+)/$', CategoryDetails.as_view(), name="category-details"),
    url(r'^(?P<pk>\d+)/edit/$', CategoryUpdate.as_view(), name="category-update"),
    url(r'^(?P<pk>\d+)/delete/$', CategoryDelete.as_view(), name="category-delete"),
    url(r'^add/$', CategoryCreate.as_view(), name="category-create"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
