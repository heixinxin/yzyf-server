__author__ = '星空大师'
__date__ = '2019/7/5 0005 19:28'

from rest_framework import serializers
from homeapi.models import HomeJob, User


class HomeSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = HomeJob
        fields = ('owner', 'url', 'id', 'name', 'price', 'job_number', 'job_number_count', 'job_require', 'company_info', 'company', 'place', 'eat', 'live', 'update_time', 'create_time')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id', 'alipay', 'gender', 'email',  'phone', 'username', 'userAdmin', 'perAdmin')
