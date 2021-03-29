from .celery import app


# 任务1
@app.task
def banner_update():
    from home import models
    from home import serialiser
    from django.core.cache import cache
    from django.conf import settings
    queryset_banner = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('order')[
               :settings.BANNER_COUNTER]
    serializer_banner = serialiser.BannerModelSerializer(instance=queryset_banner, many=True)
    # 拼接地址
    for banner in serializer_banner.data:
        banner['img'] = f"http://{settings.SET_PATH}:{settings.PORT}"+banner['img']
    cache.set('banner_list', serializer_banner.data)

    return True
