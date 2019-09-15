from django_redis import get_redis_connection
from rest_framework.pagination import PageNumberPagination
from homeapi.serializers import HomeSerializer
from myapi.forms import UploadImageForm
from myapi.models import Feedback, AuthUser
from myapi.serializers import ApplyJobSerializer
from utils.baseAuthentication import APIViewAuth, AuthenticationAll
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import json
from django.views.generic import View
from homeapi.models import User, ApplyJob, HomeJob
from django.views.decorators.csrf import csrf_exempt
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


def get_favorite_key(request):
    user = request.user
    conn = get_redis_connection('default')
    favorite_key = 'favorite_%d' % user.id
    return conn, favorite_key


# 查询申请的工作
class MyApplyView(APIViewAuth):

    def get(self, request):
        home_job_list = []
        user = request.user
        apply_list = ApplyJob.objects.filter(user=user).order_by('-create_time')
        if apply_list:
            for apply in apply_list:
                home_list = HomeSerializer(HomeJob.objects.filter(id=apply.job.id), many=True, context={'request': request}).data
                home_list[0]["status"] = apply.status
                home_list[0]["create_time"] = str(apply.create_time)[:-7]
                home_job_list.append(home_list)

            return JsonResponse({'success': 'ok', 'ApplyList': home_job_list})
        else:
            return JsonResponse({'success': 'no'})


class UserFavoriteView(APIViewAuth):

    def get(self, request, job_id):
        conn, favorite_key = get_favorite_key(request)
        # 先获取job_key的值，有值就是收藏了 none就是没收藏
        favorite_value = conn.hget(favorite_key, job_id)
        if favorite_value:
            return JsonResponse({'success': 'ok'})
        else:
            return JsonResponse({'success': 'no'})

    def post(self, request):
        job_id = json.loads(request.body.decode('utf-8'))["job_id"]
        conn, favorite_key = get_favorite_key(request)
        # 先获取job_key的值，有值就是收藏了 none就是没收藏
        favorite_value = conn.hget(favorite_key, job_id)
        if favorite_value:
            conn.hdel(favorite_key, job_id)
            return JsonResponse({'success': 'no'})
        conn.hset(favorite_key, job_id, job_id)
        return JsonResponse({'success': 'ok'})


class UserFavoriteListView(APIViewAuth):

    def get(self, request):
        conn, favorite_key = get_favorite_key(request)
        # {'岗位id':岗位id}
        favorite_dict = conn.hgetall(favorite_key)
        if not favorite_dict:
            return JsonResponse({'success': 'no'})
        favorite_list = []

        for job_id, value in favorite_dict.items():
            favorite = HomeSerializer(HomeJob.objects.filter(id=int(value)), many=True, context={'request': request}).data
            favorite_list.insert(0, favorite)

        return JsonResponse({'success': 'ok', 'favoriteList': favorite_list})


# 商家查看哪些人申请了
class MyJobPerView(APIViewAuth):

    def get(self, request, job_id):
        if not HomeJob.objects.get(id=job_id).owner == request.user:
            return JsonResponse({'msg': '您没有权限查看'})
        ApplyList = ApplyJob.objects.filter(job=job_id)
        if ApplyList:
            # many=True 表示多对多关系 设置为True
            return JsonResponse(
                {'success': 'ok', 'ApplyList': ApplyJobSerializer(ApplyList, many=True).data})
        else:
            return JsonResponse({'success': 'no'})


# 是否录取
class StatusView(APIViewAuth):

    def get(self, request, por_id):
        job = ApplyJob.objects.get(id=por_id)
        if job.status == 1:
            job.status = 2
        else:
            job.status = 1
        job.save()
        return JsonResponse({'success': 'ok'})


# 用户反馈
class FeedbackView(APIViewAuth):

    def post(self, request):
        user = request.user
        feedback = json.loads(request.body.decode('utf-8'))["feedback"]
        try:
            a = Feedback.objects.create(user=user, feedback=feedback)
            a.save()
            return JsonResponse({'success': 'ok'})
        except:
            return JsonResponse({'success': 'no'})


# 获取认证信息
from django.core.files.base import ContentFile
class AuthUserView(APIViewAuth):

    def post(self, request):
        try:
            if AuthUser.objects.get(user=request.user):
                return JsonResponse({"success": "已被注册"})
        except:
            image = request.FILES.get('face_photo')
            imag1 = request.FILES.get('word_photo')
            name = request.POST.get('name')
            card_id = request.POST.get('card_id')
            try:
                authUser = AuthUser.objects.create(user=request.user)
                authUser.face_photo.save(image.name, ContentFile(image.read()))
                authUser.word_photo.save(imag1.name, ContentFile(imag1.read()))
                authUser.name = name
                authUser.card_id = card_id
                authUser.save()
                return JsonResponse({"success": "ok"})
            except:
                return JsonResponse({"success": "no"})
