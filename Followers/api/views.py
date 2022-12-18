from django.shortcuts import get_object_or_404
from datetime import date
from django.db.models import Q
from rest_framework.serializers import ValidationError
from rest_framework import generics
from Api.models import Followers
from .serializers import (
    CreateSerializer,
    AllDataSerializer
)

model_name = Followers


class FollowList(generics.ListAPIView):
    queryset = model_name.objects.all()
    serializer_class = AllDataSerializer


def follow(request, flr, flg):
    res = Followers.objects.filter(Q(follower_id=flr) & Q(following_id=flg))
    if res:
        res = res.first()
        return FollowDetails.as_view(**{'i': res.id})(request)
    else:
        raise ValidationError("This Rating Not Exit")


class FollowDetails(generics.RetrieveAPIView):
    queryset = model_name.objects.all()
    i = None

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.get(pk=self.i)
    serializer_class = AllDataSerializer


def follow_delete(request, flr, flg):
    res = Followers.objects.filter(Q(follower_id=flr) & Q(following_id=flg))
    if res:
        res = res.first()
        return FollowDetails.as_view(**{'i': res.id})(request)
    else:
        raise ValidationError("This Rating Not Exit")


class FollowDelete(generics.DestroyAPIView):
    queryset = model_name.objects.all()
    i = None

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.get(pk=self.i)
    serializer_class = CreateSerializer


class FollowCreate(generics.CreateAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer

    def perform_create(self, serializer):
        serializer.save(created_at=date.today())