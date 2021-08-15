#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser #장고에서 사용되는 기본모델
from django.conf import settings
# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user" #db의 이름(정보)를 넣어주는 역할

    bio = models.CharField(max_length=256, default='') # 기본모델에 bio만을 추가한것
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
