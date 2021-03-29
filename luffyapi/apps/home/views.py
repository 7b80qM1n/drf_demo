from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from . import serialiser
from . import models
from django.conf import settings
from django.core.cache import cache


class BannerView(GenericViewSet, ListModelMixin):
    """
    list:
        返回个数为配置的轮播图

    """
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('order')[
               :settings.BANNER_COUNTER]
    serializer_class = serialiser.BannerModelSerializer

    def list(self, request, *args, **kwargs):
        # 获取缓存是否存在
        banner_list = cache.get('banner_list')
        if not banner_list:
            # 去数据库拿
            response = super().list(request, *args, **kwargs)
            # 加入缓存
            cache.set('banner_list', response.data, 60*60)
            return response
        return Response(data=banner_list)
