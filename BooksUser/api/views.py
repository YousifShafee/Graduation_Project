from rest_framework import generics
from django.db.models import Q
from rest_framework.serializers import ValidationError
from datetime import date
from Api.models import BooksUser
from .serializers import (
    CreateSerializer,
    AllDataSerializer
)

model_name = BooksUser


class BookUserList(generics.ListAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer


def book_user(request, book, user):
    res = BooksUser.objects.filter(Q(book=book) & Q(user=user))
    if res:
        res = res.first()
        return BookUserDetails.as_view(**{'i': res.id})(request)
    else:
        raise ValidationError("This Rating Not Exit")


class BookUserDetails(generics.RetrieveAPIView):
    queryset = model_name.objects.all()
    i = None

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.get(pk=self.i)
    serializer_class = AllDataSerializer


class BookUserDelete(generics.DestroyAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer


class BookUserUpdate(generics.RetrieveUpdateAPIView):
    queryset = model_name.objects.all()
    serializer_class = AllDataSerializer

    def perform_update(self, serializer):
        serializer.save(updated_at=date.today())


class BookUserCreate(generics.CreateAPIView):
    queryset = model_name.objects.all()
    serializer_class = AllDataSerializer

    def perform_create(self, serializer):
        serializer.save(created_at=date.today())
