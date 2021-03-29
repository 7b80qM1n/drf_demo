from celery import Celery
from django.conf import settings
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.settings.dev')
django.setup()

broker = f'redis://:{settings.REDIS_PASS}@{settings.SET_PATH}:6379/1'  # 任务队列
backend = f'redis://:{settings.REDIS_PASS}@{settings.SET_PATH}:6379/2'  # 结构存储


home_task = 'celery_task.home_task'

app = Celery(__name__, broker=broker, backend=backend, include=[home_task, ])

# 定时任务
# 时区
app.conf.timezone = 'Asia/Shanghai'

# 是否使用utc时间
app.conf.enable_utc = False

# 定时任务配置
from datetime import timedelta
from celery.schedules import crontab

app.conf.beat_schedule = {
    'low-task': {
        'task': f'{home_task}.banner_update',
        'schedule': timedelta(seconds=10),
        # 'schedule': crontab(hour=8, day_of_week=1),  # 每周一早八点
        # 'args': (1, 150),
    }
}


