from rest_framework.serializers import ModelSerializer, ValidationError
from Api.models import Followers


class AllDataSerializer(ModelSerializer):
    class Meta:
        model = Followers
        fields = [
            'follower_id',
            'following_id',
        ]


class CreateSerializer(ModelSerializer):
    class Meta:
        model = Followers
        exclude = ('id', 'created_at')

    def validate(self, request):
        flr = request['follower_id']
        flg = request['following_id']
        if flr == flg:
            raise ValidationError("Users Can't be Equal")
        return request
