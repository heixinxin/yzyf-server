__author__ = '星空大师'
__date__ = '2019/7/5 0005 16:40'

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from homeapi import views


from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'job', views.HomeJobViewSet)
router.register(r'myjob', views.MyHomeJobViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('apply', views.ApplyJobView.as_view(), name="homeApply")
]