from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from .views import (
    UserList,
    UserDetails,
    UserDelete,
    UserUpdate,
    UserLoginAPIView,
    Logout,
    UserCreateAPIView,
    my_book,
    follow,
    delete,
)

app_name = 'Users'

urlpatterns = [
    url(r'^$', UserList.as_view(), name="user-list"),
    url(r'^(?P<pk>\d+)/$', UserDetails.as_view(), name="user-details"),
    url(r'^(?P<pk>\d+)/edit/$', UserUpdate.as_view(), name="user-update"),
    url(r'^(?P<pk>\d+)/delete/$', UserDelete.as_view(), name="user-delete"),
    url(r'^add/$', UserCreateAPIView.as_view(), name="user-create"),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^mybook/$', my_book, name='my_book'),
    url(r'^follow/$', follow, name='follow'),
    url(r'^delete/$', delete, name='delete_follow'),
]
urlpatterns = format_suffix_patterns(urlpatterns)