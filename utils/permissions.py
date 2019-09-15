__author__ = '星空大师'
__date__ = '2019/7/5 0005 16:39'

from rest_framework import permissions, exceptions
from homeapi.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限，只允许对象的所有者编辑它。
    """

    #  对表权限 (这里限制post请求)
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.userAdmin:
            return True
        else:
            raise exceptions.AuthenticationFailed('你还不是商家哟')

    #  对单个的权限
    def has_object_permission(self, request, view, obj):
        # 任何用户或者游客都可以访问任何岗位, 所以请求动作在安全范围内
        # 所以我们总是允许GET、HEAD或OPTIONS请求。
        # 必须是商家才能发布需求
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.userAdmin:
            # 而当请求不是上面的安全模式的话， 那就需要判断一下当前的用户
            # 如果岗位所有者和当前的用户一致，那就允许，否则返回错误信息
            return obj.owner == request.user
        else:
            raise exceptions.AuthenticationFailed('你还不是商家哟')
