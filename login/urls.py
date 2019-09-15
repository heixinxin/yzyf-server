__author__ = '星空大师'
__date__ = '2019/7/8 0008 21:56'


from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name="register"),
    path('login', views.LoginView.as_view(), name="login"),
    path('getuser', views.getUserView.as_view(), name="getuser"),
    path('modifyPwd', views.modifyPwdView.as_view(), name="modifyPwd"),
    path('putGender', views.putGender.as_view(), name="putGender"),
    path('putEmail', views.putEmail.as_view(), name="putEmail"),
]