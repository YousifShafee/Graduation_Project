from django.conf.urls import url
from .views import (
    ReviewsList,
    ReviewsDetails,
    ReviewsUpdate,
    ReviewsDelete,
    ReviweCreate
)
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'Review'

urlpatterns = [
    url(r'^$', ReviewsList.as_view(), name="Reviews-list"),
    url(r'^(?P<pk>\d+)/$', ReviewsDetails.as_view(), name="Reviews-details"),
    url(r'^(?P<pk>\d+)/edit/$', ReviewsUpdate.as_view(), name="Reviews-update"),
    url(r'^(?P<pk>\d+)/delete/$', ReviewsDelete.as_view(), name="Reviews-delete"),
    url(r'^add/$', ReviweCreate.as_view(), name="Reviews-create"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
