
from django.db import models

# Create your models here.
from db.base_model import BaseModel
from homeapi.models import User
from datetime import datetime



class Feedback(BaseModel, models.Model):
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    feedback = models.CharField(max_length=200, verbose_name=u"用户反馈")

    class Meta:
        db_table = 'yz_Feedback'
        verbose_name = u'用户反馈'
        verbose_name_plural = verbose_name


class AuthUser(BaseModel, models.Model):
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=20, verbose_name=u"用户真实姓名")
    card_id = models.CharField(default="", max_length=30, verbose_name=u"身份证")
    face_photo = models.ImageField(default="", max_length=100, upload_to="IDNumber/%Y/%m/%d", verbose_name=u"身份证人脸照")
    word_photo = models.ImageField(default="", max_length=100, upload_to="IDNumber/%Y/%m/%d", verbose_name=u"身份证国徽照")

    class Meta:
        db_table = 'yz_AuthUser'
        verbose_name = u"认证信息"
        verbose_name_plural = verbose_name

#  邮箱验证码表
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_time = models.DateTimeField(verbose_name=u'发送时间', default=datetime.now)  # 发送验证码的时间

    class Meta:
        db_table = 'yz_email'
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name