# Create your views here.
import json

from django.db.models import Q
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from homeapi.models import User, HomeJob, ApplyJob
from homeapi.serializers import HomeSerializer, UserSerializer
from rest_framework import permissions, exceptions
from utils.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utils.baseAuthentication import AuthenticationAll, APIViewAuth


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    这个视图集自动提供list和detail操作
    """
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination


class HomeJobViewSet(viewsets.ModelViewSet):
    """
    这个视图集自动提供list、create、retrieve，岗位list
    """
    queryset = HomeJob.objects.all().order_by("-create_time")
    serializer_class = HomeSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyHomeJobViewSet(HomeJobViewSet, AuthenticationAll):
    """
    商家发布的所有需求的list视图
    """

    def get_queryset(self):
        if self.request.user.userAdmin:
            home_list = HomeJob.objects.filter(owner__username=self.request.user.username).order_by("-update_time")
            if home_list:
                return home_list
            else:
                raise exceptions.APIException({"msg": "您还没有发布需求哟"})
        else:
            raise exceptions.APIException({"msg": "您还不是商家哟"})


class ApplyJobView(APIViewAuth):
    """
    申请工作视图
    """
    def post(self, request):
        user = request.user
        apply = json.loads(request.body.decode('utf-8'))
        try:
            job = HomeJob.objects.get(id=int(apply["job"]))
            user_job = ApplyJob.objects.filter(Q(job=job) & Q(user=user))
            if user_job:
                return JsonResponse({"success": "nok"})
            ApplyJob.objects.create(
                job=job,
                user=user,
                name=apply["name"],
                gender=apply["gender"],
                age=int(apply["age"]),
                card_id=apply["card_id"],
                number=apply["number"]
            )
            job.job_number_count += 1
            job.save()
            return JsonResponse({"success": "ok"})
        except:
            return JsonResponse({"success": "no"})
