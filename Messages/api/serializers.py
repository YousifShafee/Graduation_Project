from rest_framework.serializers import ModelSerializer
from Api.models import Messages


class CreateSerializer(ModelSerializer):
    class Meta:
        model = Messages
        exclude = ('created_at', 'updated_at')


class AllDataSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
