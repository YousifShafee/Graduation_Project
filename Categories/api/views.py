from datetime import date
from rest_framework import generics
from Api.models import Categories
from .serializers import (
    BookCategorySerializer,
    CategoriesSerializer,
    CategoriesAllDataSerializer,
)

model_name = Categories


class CategoryList(generics.ListAPIView):
    queryset = model_name.objects.all()
    serializer_class = CategoriesSerializer


class CategoryDetails(generics.RetrieveAPIView):
    queryset = model_name.objects.all()
    serializer_class = CategoriesSerializer


class CategoryDelete(generics.DestroyAPIView):
    queryset = model_name.objects.all()
    serializer_class = CategoriesSerializer


class CategoryUpdate(generics.RetrieveUpdateAPIView):
    queryset = model_name.objects.all()
    serializer_class = CategoriesAllDataSerializer

    def perform_update(self, serializer):
        serializer.save(updated_at=date.today())


class CategoryCreate(generics.CreateAPIView):
    queryset = model_name.objects.all()
    serializer_class = CategoriesSerializer

    def perform_create(self, serializer):
        serializer.save(created_at=date.today())
