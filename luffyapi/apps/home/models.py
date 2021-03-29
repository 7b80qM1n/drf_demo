from django.db import models
from luffyapi.utils.models import BaseModel


class Banner(BaseModel):
    name = models.CharField(verbose_name='图片名字', max_length=32)
    img = models.ImageField(verbose_name='轮播图', help_text='图片尺寸必须是3840*800', upload_to='banner', null=True)
    link = models.CharField(verbose_name='跳转连接', max_length=32)
    info = models.TextField(verbose_name='图片简介')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = "轮播图"
