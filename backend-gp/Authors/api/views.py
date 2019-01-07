from datetime import date
from rest_framework import generics
from Api.models import Authors, Books
from .serializers import (
    AuthorsCreateSerializer,
    # BookSerializer,
    AuthorsAllDataSerializer
)

model_name = Authors


class AuthorList(generics.ListAPIView):
    queryset = model_name.objects.all()
    serializer_class = AuthorsCreateSerializer


class AuthorDetails(generics.RetrieveAPIView):
    queryset = model_name.objects.all()
    serializer_class = AuthorsCreateSerializer


class AuthorDelete(generics.DestroyAPIView):
    queryset = model_name.objects.all()
    serializer_class = AuthorsCreateSerializer


class AuthorCreate(generics.CreateAPIView):
    queryset = model_name.objects.all()
    serializer_class = AuthorsCreateSerializer

    def perform_create(self, serializer):
        serializer.save(created_at=date.today())


class AuthorUpdate(generics.RetrieveUpdateAPIView):
    queryset = model_name.objects.all()
    serializer_class = AuthorsAllDataSerializer

    def perform_update(self, serializer):
        serializer.save(updated_at=date.today())
