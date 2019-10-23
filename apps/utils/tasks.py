
__author__ = '星空大师'
__date__ = '2019/6/10 0010 19:51'

# 使用celery
from django.core.mail import send_mail
from yzyf import settings
from celery import Celery
import time
from random import Random


# 在任务处理者一端加这几句
import os
import django
#　引用模块要放在这下面 否则pychame找不到
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yzyf.settings")
django.setup()

from myapi.models import EmailVerifyRecord
from django_redis import get_redis_connection
from homeapi.models import User


# 创建一个Celery类的实例对象
app = Celery('utils.tasks', broker='redis://localhost:6379/8')


def random_str(randomlength=4):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'   # 让我们的验证码从这些字符串中 随机选几个
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]   # 随机选一个数  字符串进行拼接
    return str


@app.task
def send_email_code(to_email):
    '''发送激活邮件'''
    # 组织邮件信息
    code = random_str(4)
    email_record = EmailVerifyRecord()
    if EmailVerifyRecord.objects.filter(email=to_email):
        EmailVerifyRecord.objects.filter(email=to_email).update(
            code=code
        )
    else:
        email_record.code = code
        email_record.email = to_email
        email_record.save()
    subject = 'yzyf在线修改邮箱验证码'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = "你的邮箱验证码为: {0}".format(code)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)

@app.task
def send_pwd(to_email):

    subject = 'yzyf找回密码'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    if User.objects.get(email=to_email):
        html_message = "很抱歉，您没有绑定邮箱！请联系客服找回密码。"
    else:
        html_message = "您的上一个密码是：{0}".format()
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)