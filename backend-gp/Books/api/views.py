from rest_framework.decorators import api_view
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import date
from rest_framework import generics
from Recommend.views import cached_user
from Api.models import Books
from .serializers import (
    BooksCreateSerializer,
    AllDataSerializer,
    RateSerializer,
    RecentSerializer,
)
from .data import main

model_name = Books
value = {
        'rate': RateSerializer,
        'recent': RecentSerializer,
    }


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def most_recent_l():
    with connection.cursor() as cursor:
        cursor.execute("SELECT books.id, books.book_name, books.img, left(books.book_desc, 100) as description, "
                       "avg(ratings.value) as avg FROM books, ratings where ratings.book=books.id "
                       "group by books.id order by books.created_at DESC limit 12")
        name = dictfetchall(cursor)
    return name


def most_rated_l():
    with connection.cursor() as cursor:
        cursor.execute("SELECT books.id, books.book_name, books.img, left(books.book_desc, 100) as description, "
                       "avg(ratings.value) as avg FROM books, ratings where ratings.book=books.id "
                       "group by books.id order by avg DESC limit 12")
        name = dictfetchall(cursor)
    return name


@api_view(['GET'])
def books(request, pk):
    reco = cached_user(pk)
    recent = most_recent_l()
    rate = most_rated_l()
    return Response({"Recommend": reco[:10], "Recent": recent, "Rate": rate}, status=status.HTTP_201_CREATED)


def index_list(request, var):
    data = value[var]
    return IndexList.as_view(**{'serializer_class': data})(request)


class IndexList(generics.RetrieveAPIView):
    queryset = model_name.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=1)
        return obj


def book_list(request):
    return BookList.as_view()(request)


class BookList(generics.ListAPIView):
    queryset = model_name.objects.all()
    serializer_class = BooksCreateSerializer


@api_view(['GET'])
def book_details(request, pk):
    return Response(main(pk), status=status.HTTP_201_CREATED)


class BookDelete(generics.DestroyAPIView):
    queryset = model_name.objects.all()
    serializer_class = AllDataSerializer


class BookCreate(generics.CreateAPIView):
    queryset = model_name.objects.all()
    serializer_class = AllDataSerializer

    def perform_create(self, serializer):
        serializer.save(created_at=date.today())


class BookUpdate(generics.RetrieveUpdateAPIView):
    queryset = model_name.objects.all()
    serializer_class = AllDataSerializer

    def perform_update(self, serializer):
        serializer.save(updated_at=date.today())
