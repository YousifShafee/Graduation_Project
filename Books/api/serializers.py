from rest_framework.serializers import ModelSerializer
from Api.models import Books, Users
from Categories.api.serializers import BookCategorySerializer
from Authors.api.serializers import AuthorsNameCreateSerializer


class BooksCreateSerializer(ModelSerializer):
    category = BookCategorySerializer(read_only=True)
    author = AuthorsNameCreateSerializer(read_only=True)

    class Meta:
        model = Books
        fields = [
            'id',
            'book_name',
            'img',
            'author',
            'category',
            'avg_rating',
            'user_rating',
            'user_status',
            'same_author',
            'book_desc',
            'review_count',
            'review',
        ]


class BooksAllDataSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = ['id', 'book_name']


class AllDataSerializer(ModelSerializer):
    class Meta:
        model = Books
        exclude = ('id', 'created_at', 'updated_at', 'deleted_at')


class RateSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['most_rated']


class RecentSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['most_recent']
