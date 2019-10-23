__author__ = '星空大师'
__date__ = '2019/9/6 0006 22:04'

from django import forms
from myapi.models import AuthUser


# 图片验证 直接通过上传的路径
class UploadImageForm(forms.ModelForm):
   class Meta:
      model = AuthUser
      fields = ['face_photo']
