from rest_framework.serializers import ModelSerializer
from Api.models import Authors


class AuthorsCreateSerializer(ModelSerializer):
    class Meta:
        model = Authors
        fields = [
            'id',
            'author_name',
            'author_bio',
            'birthday',
            'img',
            'header_img',
            'avg_all',
            'book_name',
			'follower',
            'face_icon',
            'twitter_icon',
            'website',
        ]


class AuthorsNameCreateSerializer(ModelSerializer):
    class Meta:
        model = Authors
        fields = ['id', 'author_name']


class AuthorsAllDataSerializer(ModelSerializer):
    class Meta:
        model = Authors
        exclude = ('id', 'created_at', 'updated_at', 'deleted_at')
