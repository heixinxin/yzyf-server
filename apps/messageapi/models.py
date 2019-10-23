from django.db import models
from db.base_model import BaseModel
from homeapi.models import HomeJob, User
# Create your models here.


class UserMessage(BaseModel, models.Model):
    user = models.IntegerField(default=0, verbose_name=u'接受用户')
    sj_user = models.IntegerField(verbose_name=u'发送用户')
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")

    class Meta:
        db_table = 'yz_User_Message'
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class JobComment(BaseModel, models.Model):
    job = models.ForeignKey(HomeJob, null=True, blank=True, verbose_name=u"岗位", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name=u"评论")

    class Meta:
        db_table = 'yz_User_JobComment'
        verbose_name = u'用户评论'
        verbose_name_plural = verbose_name


class UserFavorite(BaseModel, models.Model):
    job = models.ForeignKey(HomeJob, null=True, blank=True, verbose_name=u"岗位", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)

    class Meta:
        db_table = 'yz_User_Favorite'
        verbose_name = u'收藏岗位'
        verbose_name_plural = verbose_name
