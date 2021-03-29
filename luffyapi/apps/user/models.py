from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    telephone = models.CharField(verbose_name='电话号码', max_length=11)
    icon = models.ImageField(verbose_name='默认头像', upload_to='icon', default='icon/default.png')

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username