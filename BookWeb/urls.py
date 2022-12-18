from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/cate/', include('Categories.api.urls', namespace='category')),
    url(r'^api/user/', include('Users.api.urls', namespace='user')),
    url(r'^api/book/', include('Books.api.urls', namespace='book')),
    url(r'^api/author/', include('Authors.api.urls', namespace='author')),
    url(r'^api/mess/', include('Messages.api.urls', namespace='message')),
    url(r'^api/follow/', include('Followers.api.urls', namespace='follower')),
    url(r'^api/book_user/', include('BooksUser.api.urls', namespace='book_user')),
    url(r'^api/rating/', include('Rating.api.urls', namespace='rating')),
    url(r'^api/review/', include('Review.api.urls', namespace='review')),
    url(r'^api/reco/', include('Recommend.urls')),
    url(r'^api/', include('Api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
