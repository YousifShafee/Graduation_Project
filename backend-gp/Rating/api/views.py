from rest_framework import generics
from django.db.models import Q
from rest_framework.serializers import ValidationError
from datetime import date
from Api.models import Ratings
from .serializers import (
    CreateSerializer,
    AllDataSerializer
)

model_name = Ratings


class RatingsList(generics.ListAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer


def rating_list(request, book, user):
    res = Ratings.objects.filter(Q(book=book) & Q(user=user))
    if res:
        res = res.first()
        return RatingsDetails.as_view(**{'i': res.id})(request)
    else:
        raise ValidationError("This Rating Not Exit")


class RatingsDetails(generics.RetrieveAPIView):
    queryset = model_name.objects.all()
    i = None

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.get(pk=self.i)
    serializer_class = AllDataSerializer


class RatingsDelete(generics.DestroyAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer


class RatingsUpdate(generics.RetrieveUpdateAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer

    def perform_update(self, serializer):
        serializer.save(updated_at=date.today())


class RatingsCreate(generics.CreateAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer

    def perform_create(self, serializer):
        serializer.save(created_at=date.today())


'''
def index_list(request, var):
    data = value[var]
    return IndexList.as_view(**{'serializer_class': data})(request)


class IndexList(generics.RetrieveAPIView):
    queryset = model_name.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=1)
        return obj
        
'''