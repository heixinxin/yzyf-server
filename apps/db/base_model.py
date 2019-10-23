__author__ = '星空大师'
__date__ = '2019/7/5 0005 16:15'

from django.db import models


class BaseModel(models.Model):
    """
    模型抽象基类
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name=u"更新时间")

    class Meta:
        # 说明是一个抽象模型类
        abstract = True