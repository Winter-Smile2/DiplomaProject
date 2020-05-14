import random

from django.db import models



# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=11, verbose_name='用户名', primary_key=True)
    nickname = models.CharField(max_length=30,verbose_name='昵称')
    email = models.EmailField(verbose_name='邮箱')
    password = models.CharField(max_length=32, verbose_name='密码')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    login_time = models.DateTimeField(null=True, verbose_name='登录时间')

    class Meta:
        db_table = 'user_profile'





