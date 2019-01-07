from django.conf.urls import url
from .views import (
    RatingsList,
    RatingsDetails,
    RatingsUpdate,
    RatingsDelete,
    RatingsCreate,
    rating_list
)
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'Rating'

urlpatterns = [
    url(r'^$', RatingsList.as_view(), name="Ratings-list"),
    url(r'^add/$', RatingsCreate.as_view(), name="Ratings-create"),
    url(r'^(?P<book>\d+)/(?P<user>\d+)/$', rating_list, name="Ratings-details"),
    url(r'^(?P<pk>\d+)/edit/$', RatingsUpdate.as_view(), name="Ratings-update"),
    url(r'^(?P<pk>\d+)/delete/$', RatingsDelete.as_view(), name="Ratings-delete"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
