from rest_framework_jwt.settings import api_settings
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login as auth_login, logout
from rest_framework.views import APIView
from datetime import date, datetime
from Api.models import Users, Followers
from .serializers import (
    UsersSerializer,
    UsersNameDataSerializer,
    AllDataSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    MyBookSerializer,
)

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

model_name = Users


class UserList(generics.ListAPIView):
    queryset = model_name.objects.all()
    serializer_class = UsersSerializer


def follow(request):
    flr = request.user.id
    flg = 1
    follower = Followers.objects.filter(Q(follower_id=flr) & Q(following_id=flg)).distinct()
    if follower.exists():
        raise ValueError("This User in your Followers Already")
    crt = date.today()
    Followers(follower_id=flr, following_id=flg, created_at=crt).save()
    return UserDetails.as_view()(request)


def delete(request):
    return UserDetails.as_view(**{'user_id': request.user.id})(request)


class UserDetails(generics.RetrieveAPIView):
    queryset = model_name.objects.all()
    serializer_class = UsersSerializer


def my_book(request):
    return MyBook.as_view(**{'user_id': request.user.id})(request)


class MyBook(generics.RetrieveAPIView):
    queryset = model_name.objects.all()
    user_id = None

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.user_id)
        return obj
    serializer_class = MyBookSerializer


class UserDelete(generics.DestroyAPIView):
    queryset = model_name.objects.all()
    serializer_class = UsersSerializer


class UserUpdate(generics.RetrieveUpdateAPIView):
    queryset = model_name.objects.all()
    serializer_class = AllDataSerializer

    def perform_update(self, serializer):
        serializer.save(updated_at=date.today())


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = Users.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(created_at=date.today())


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()
    serializer_class = UserLoginSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'view': self,
        }

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer.validate(self, data=request.data)

        if serializer:
            user = serializer['user'] or request.user
            token = serializer['token']
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            login(request)
            response.data['id'] = user.id
            response.data['username'] = user.username
            response.data['img'] = user.img
            return response

        return Response("Incorrect credentials, Please Try Again", status=HTTP_400_BAD_REQUEST)


def login(request):
    msg = []
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return msg.append("login successful")
        else:
            return msg.append("disabled account")
    else:
        return msg.append("invalid login")


class Logout(APIView):
    queryset = Users.objects.all()
    def get(self, request, format=None):
        # request.user.auth_token.delete()
        logout(request)
        return Response(status=HTTP_200_OK)
