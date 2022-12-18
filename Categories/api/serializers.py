from rest_framework.serializers import ModelSerializer
from Api.models import Categories


class BookCategorySerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'cate_name']


class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            'id',
            'cate_name',
            'cate_desc',
            'most_recent',
            'most_read',
            'most_rated',
        ]


class CategoriesAllDataSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = ['cate_name', 'cate_desc']
