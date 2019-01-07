from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from Api.models import Users
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError,
)
import jwt
from django.utils.translation import ugettext as _
from .compat import Serializer

from rest_framework_jwt.compat import get_username_field, PasswordField

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class UserCreateSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label='Email')
    password = CharField(style={'input_type': 'password'})

    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'token',
            'full_name',
            'email',
            'password',
            'img',
            'address',
            'city_town',
            'country',
            'birthday',
            'gender',
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        email = data['email']
        user_qs = Users.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This Email has already registered.")
        username = data['username']
        password = data['password']
        user_na = Users.objects.filter(username=username)
        if user_na.exists():
            raise ValidationError("This Username has already Used.")
        if username == password:
            raise ValidationError("Password Can't be equal to Username.")
        if len(password) < 8:
            raise ValidationError("Password Can't be less than 8 character.")
        return data

    def create(self, validated_data):
        username = validated_data['username']
        full_name = validated_data['full_name']
        email = validated_data['email']
        password = validated_data['password']
        img = validated_data['img']
        address = validated_data['address']
        city_town = validated_data['city_town']
        country = validated_data['country']
        birthday = validated_data['birthday']
        gender = validated_data['gender']
        user_obj = Users(
            username=username,
            email=email,
            full_name=full_name,
            img=img,
            address=address,
            city_town=city_town,
            country=country,
            birthday=birthday,
            gender=gender,
        )
        user_obj.set_password(password)
        user_obj.save()
        user_qs = Users.objects.get(username=username)
        user = authenticate(username=username, password=password)
        payload = jwt_payload_handler(user)
        validated_data['token'] = jwt_encode_handler(payload)
        validated_data['id'] = user_qs.id
        validated_data['password'] = '*****'
        del validated_data['full_name']
        del validated_data['address']
        del validated_data['city_town']
        del validated_data['country']
        del validated_data['birthday']
        del validated_data['gender']
        result = {'token': jwt_encode_handler(payload), 'user': user}
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=False, label='Username')
    password = CharField(allow_blank=True, style={'input_type': 'password'})
    img = CharField(allow_blank=False, read_only=True)

    class Meta:
        model = Users
        fields = [
            'id',
            'token',
            'username',
            'password',
            'img',
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data.get('username')
        password = data['password']

        if not username:
            raise ValidationError("The Username is required")
        user = Users.objects.get(username=username)
        if user :
            if not user.check_password(password):
                raise ValidationError("Incorrect credentials, Please Try Again")
        else:
            raise ValidationError("This Usernameis not valid")

        user = authenticate(username=username, password=password)
        payload = jwt_payload_handler(user)
        result = {'token': jwt_encode_handler(payload), 'user': user}
        return result


class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'email',
            'img',
            'birthday',
            'gender',
            'avg_all',
            'book',
            'ip',
            'last_login',
            'book'
        ]


class MyBookSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'book',
            'read',
            'current_read',
            'to_read',
        ]


class UsersNameDataSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username']


class AllDataSerializer(ModelSerializer):
    class Meta:
        model = Users
        exclude = ('password', 'active', 'staff', 'admin', 'ip', 'last_login', 'created_at', 'updated_at', 'deleted_at')
