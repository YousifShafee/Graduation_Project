from rest_framework.serializers import ModelSerializer
from Api.models import Ratings
from Books.api.serializers import BooksAllDataSerializer
from Users.api.serializers import UsersNameDataSerializer


class CreateSerializer(ModelSerializer):
    book = BooksAllDataSerializer(read_only=True)
    user = UsersNameDataSerializer(read_only=True)

    class Meta:
        model = Ratings
        fields = [
            'id',
            'book',
            'user',
            'value',
            'avrg',
        ]


class AllDataSerializer(ModelSerializer):
    class Meta:
        model = Ratings
        fields = [
            'book',
            'user',
            'value',
        ]

