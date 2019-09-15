__author__ = '星空大师'
__date__ = '2019/7/8 0008 16:49'

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from homeapi import views
from utils.RewriteAuthToken import ObtainAuthTokenFixed



from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'homejob', views.HomeJobViewSet)
# router.register(r'myhomejob', views.MyHomeJobViewSet)

urlpatterns = [
    path('', include(router.urls)),
]