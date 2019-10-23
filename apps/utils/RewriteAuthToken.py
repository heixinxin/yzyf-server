from abc import ABC

__author__ = '星空大师'
__date__ = '2019/7/6 0006 23:40'
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from rest_framework import serializers
from homeapi.models import User
from homeapi.serializers import UserSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomAuthTokenSerializer(AuthTokenSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                raise serializers.ValidationError({'errmsg': '兄弟，你账号或密码错了'})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


# 重写ObtainAuthToken方法，
class ObtainAuthTokenFixed(ObtainAuthToken):
    # (解决强制用csrf验证问题)
    authentication_classes = ()
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        userInfo = User.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'code': 200, 'token': token.key, 'userinfo': UserSerializer(userInfo, context={'request': request}).data})
