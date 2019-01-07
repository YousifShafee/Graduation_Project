from rest_framework.serializers import ModelSerializer
from Api.models import Reviews
from Books.api.serializers import BooksAllDataSerializer
from Users.api.serializers import UsersNameDataSerializer


class CreateSerializer(ModelSerializer):
    book = BooksAllDataSerializer(read_only=True)
    user = UsersNameDataSerializer(read_only=True)

    class Meta:
        model = Reviews
        exclude = ('created_at', 'updated_at', 'deleted_at')


class AllDataSerializer(ModelSerializer):
    class Meta:
        model = Reviews
        exclude = ('id', 'created_at', 'updated_at', 'deleted_at')
