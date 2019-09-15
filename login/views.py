__author__ = '星空大师'
__date__ = '2019/7/8 0008 21:56'
from homeapi.serializers import UserSerializer
from utils.baseAuthentication import APIViewAuth
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import json
# Create your views here.
from django.views.generic import View
from homeapi.models import User
from django.views.decorators.csrf import csrf_exempt
from utils.mixin_utils import LoginRequiredMixin

SUCCESS = {
    'code': '200',
    'data': None,
    'success': 'ok',
    'errmsg': '访问姿势不对',
}


# 重写authenticate方法 来校验登录的账号和密码
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.filter(Q(username=username) | Q(alipay=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 注册
class RegisterView(View):
    def get(self, request):
        return JsonResponse(SUCCESS, json_dumps_params={'ensure_ascii': False})

    @csrf_exempt
    def post(self, request):
        try:
            Info = json.loads(request.body.decode('utf-8'))
            user_name = Info["username"]
            pass_word = Info["password"]
            alipay = Info["alipay"]
        except:
            return JsonResponse({'success': 'no', 'errmsg': '前端数据接受失败'})

        if not all([user_name, pass_word, alipay]):
            # 数据不完整
            return JsonResponse({'success': 'no', 'errmsg': '数据不完整'})

        if User.objects.filter(Q(username=user_name) | Q(alipay=alipay)):
            return JsonResponse({'success': 'no', "errmsg": "用户名或支付宝号已存在"}, json_dumps_params={'ensure_ascii': False})
        pass_word = make_password(pass_word)
        user = User.objects.create(username=user_name, password=pass_word, alipay=alipay)
        user.save()
        return JsonResponse({'success': 'ok', 'msg': '注册成功'})


# 登录
class LoginView(View):
    def get(self, request):
        return JsonResponse(SUCCESS, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        try:
            Info = json.loads(request.body.decode('utf-8'))
            user_name = Info["username"]
            pass_word = Info["password"]
        except:
            return JsonResponse({'success': 'no', 'errmsg': '前端数据接受失败'})
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            # 用户密码正确
            # login(request, user)
            return JsonResponse({'success': 'ok', 'msg': '登录成功'})
        else:
            return JsonResponse({'success': 'no', 'errmsg': '用户名或密码错误'})


# 用户自己的信息
class getUserView(APIViewAuth):

    def get(self, request):
        user = request.user
        user_info = User.objects.get(username=user)
        return JsonResponse({'userinfo': UserSerializer(user_info, context={'request': request}).data})

    def put(self, request):
        user = request.user
        Info = json.loads(request.body.decode('utf-8'))
        try:
            username = Info["username"]
            User.objects.filter(username=user.username).update(
                username=username
            )
            return JsonResponse({"success": "ok"})
        except:
            return JsonResponse({"success": "no"})


class putGender(APIViewAuth):

    def put(self, request):
        user = request.user
        Info = json.loads(request.body.decode('utf-8'))
        try:
            gender = Info["gender"]
            User.objects.filter(username=user.username).update(
                gender=gender
            )
            return JsonResponse({"success": "ok"})
        except:
            return JsonResponse({"success": "no"})


class putEmail(APIViewAuth):

    def put(self, request):
        user = request.user
        Info = json.loads(request.body.decode('utf-8'))
        try:
            email = Info["email"]
            User.objects.filter(username=user.username).update(
                email=email
            )
            return JsonResponse({"success": "ok"})
        except:
            return JsonResponse({"success": "no"})


# 修改密码
class modifyPwdView(APIViewAuth):

    def post(self, request):
        user = request.user
        password = json.loads(request.body.decode('utf-8'))["password"]
        try:
            User.objects.filter(username=user).update(password=make_password(password))
            return JsonResponse({'success': 'ok'})
        except:
            return JsonResponse({'success': 'no'})
