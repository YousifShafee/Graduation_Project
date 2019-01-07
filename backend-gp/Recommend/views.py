from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .Algorithm import recommend
from .item import item_item

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def cached_user(user):
    if user in cache:
        books = cache.get(user)
        # convert to json

        return books
    else:
        # get data from algorithm
        books = recommend(user)
        # covert to json

        # store data in cache
        cache.set(user, books)
        return books


def cached_item(user):
    if user in cache:
        books = cache.get(user+15000)
        # convert to json

        return books
    else:
        # get data from algorithm
        books = item_item(user)
        # covert to json

        # store data in cache
        cache.set(user+15000, books)
        return books


@api_view(['GET'])
def cached_views(request, pk):

    results = cached_user(pk)
    return Response(results, status=status.HTTP_201_CREATED)

