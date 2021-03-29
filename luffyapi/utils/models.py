from django.db import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    is_show = models.BooleanField(verbose_name='是否展示', default=True)
    order = models.IntegerField(verbose_name='序号')

    class Meta:
        abstract = True  # 抽象类
