from datetime import date
from rest_framework import generics
from Api.models import Reviews
from .serializers import (
    CreateSerializer,
    AllDataSerializer
)
from rest_framework.permissions import AllowAny
from django.http import HttpResponse

model_name = Reviews


class ReviewsList(generics.ListAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer

    def post(self, request):
        book = model_name.objects.only('id').get(id=request.data['book'])
        model_name.objects.create(
            comment=request.data.get('comment'),
            book=book
        )
        return HttpResponse(status=201)


class ReviewsDetails(generics.RetrieveAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer


class ReviewsDelete(generics.DestroyAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer


class ReviewsUpdate(generics.RetrieveUpdateAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer

    def perform_update(self, serializer):
        serializer.save(updated_at=date.today())


class ReviweCreate(generics.CreateAPIView):
    queryset = model_name.objects.all()
    serializer_class = AllDataSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(created_at=date.today())
