from django.db import models

from db.base_model import BaseModel
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# 为每个用户添加token值


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# 重写默认的用户表
class User(AbstractUser):
    alipay = models.CharField(max_length=20, default="", verbose_name=u"支付宝账号")
    phone = models.CharField(max_length=11, default="", verbose_name=u"电话号码")
    gender = models.CharField(max_length=10, choices=(("male", u"男"), ("female", u"女")), default="female")
    userAdmin = models.BooleanField(default=False, verbose_name=u"商家验证")
    perAdmin = models.BooleanField(default=False, verbose_name=u"个人验证")

    class Meta:
        db_table = 'yz_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


# 兼职信息表
class HomeJob(BaseModel, models.Model):

    name = models.CharField(max_length=100, default="", verbose_name=u"岗位名称")
    price = models.CharField(max_length=50, default='10', verbose_name=u"报酬金额")
    company = models.CharField(max_length=100, default="", verbose_name=u"公司名称")
    place = models.CharField(max_length=20, default="", verbose_name=u"地点")
    job_require = models.CharField(max_length=500, default="", verbose_name=u"工作要求")
    company_info = models.CharField(max_length=500, default="", verbose_name=u"公司介绍")
    eat = models.BooleanField(default=True)
    live = models.BooleanField(default=True)
    job_number = models.IntegerField(default=0, verbose_name=u"招收人数")
    job_number_count = models.IntegerField(default=0, verbose_name=u"现有人数")
    owner = models.ForeignKey(User, related_name='homejob', on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'yz_home_job'
        verbose_name = u'兼职信息'
        verbose_name_plural = verbose_name


class ApplyJob(BaseModel, models.Model):

    job = models.ForeignKey(HomeJob, null=True, blank=True, verbose_name=u"岗位", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    name = models.CharField(max_length=10, default="", verbose_name=u"姓名")
    gender = models.CharField(max_length=10, choices=(("male", u"男"), ("female", u"女")), default="female")
    age = models.IntegerField(default="", verbose_name=u"年龄")
    card_id = models.CharField(max_length=30, default="", verbose_name=u"身份证")
    number = models.CharField(max_length=11, default="", verbose_name=u"电话号码")
    status = models.SmallIntegerField(default=1, verbose_name=u"申请状态")

    class Meta:
        db_table = 'yz_apply'
        verbose_name = u"申请信息"
        verbose_name_plural = verbose_name
