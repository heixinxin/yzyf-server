__author__ = '星空大师'
__date__ = '2019/7/8 0008 16:50'

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapi import views
from utils.RewriteAuthToken import ObtainAuthTokenFixed

from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()
# router.register(r'apply', views.MyApplyView)

urlpatterns = [
    path('', include(router.urls)),
    path('apply', views.MyApplyView.as_view(), name="myApply"),
    path('favorite/<int:job_id>', views.UserFavoriteView.as_view(), name="getfavorite"),
    path('favorite', views.UserFavoriteView.as_view(), name="favorite"),
    path('favoritelist', views.UserFavoriteListView.as_view(), name="favoritelist"),
    path('perjob/<int:job_id>', views.MyJobPerView.as_view(), name="perjob"),
    path('status/<int:por_id>', views.StatusView.as_view(), name="status"),
    path('feedback', views.FeedbackView.as_view(), name="feedback"),
    path('authuser', views.AuthUserView.as_view(), name="authuser"),

]
