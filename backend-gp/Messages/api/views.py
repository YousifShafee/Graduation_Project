from datetime import date
from rest_framework import generics
from Api.models import Messages
from .serializers import (
    CreateSerializer,
    AllDataSerializer
)

model_name = Messages


class MessageAll(generics.ListAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer


class MessageDetails(generics.RetrieveAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer


class MessageDelete(generics.DestroyAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer


class MessageUpdate(generics.RetrieveUpdateAPIView):
    queryset = model_name.objects.all()
    serializer_class = CreateSerializer

    def perform_update(self, serializer):
        serializer.save(updated_at=date.today())
