import re
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from . import serialiser
from . import models
from luffyapi.utils.response import APIResponse
from rest_framework.decorators import action
from luffyapi.libs.tencent_sms import sms
from django_redis import get_redis_connection
from .throttlings import SMSThrotting
from django.conf import settings
from rest_framework.exceptions import ValidationError

class LoginView(ViewSet):
    # 用户名邮箱手机号+密码登陆
    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        ser = serialiser.UserModelSerializer(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['user'].username
            return APIResponse(token=token, username=username)
        else:
            return APIResponse(code=0, msg=ser.errors)

    # 验证手机是否存在
    @action(methods=['GET'], detail=False)
    def check_telephone(self, request, *args, **kwargs):
        telephone = request.query_params.get('telephone')
        import re
        if not re.match('^1[3-9][0-9]{9}$', telephone):
            return APIResponse(code=0, msg='手机号不合法')
        try:
            models.User.objects.get(telephone=telephone)
            return APIResponse(code=1, msg='手机号存在')
        except:
            return APIResponse(code=2, msg='手机号不存在')

    # 验证码登陆
    @action(methods=['POST'], detail=False)
    def code_login(self, request, *args, **kwargs):
        ser = serialiser.CodeUserSerializer(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['user'].username
            return APIResponse(token=token, username=username)
        else:
            return APIResponse(code=0, msg=ser.errors)


class SendSmsView(ViewSet):
    # 频率限制
    throttle_classes = [SMSThrotting, ]

    # 登陆发送短信
    @action(methods=['GET'], detail=False)
    def send(self, request, *args, **kwargs):
        telephone = request.query_params.get('telephone')
        status = request.query_params.get('status')
        if not re.match('^1[3-9][0-9]{9}$', telephone):
            return APIResponse(code=0, msg='手机号不合法')
        user = models.User.objects.filter(telephone=telephone).first()
        if user:
            if status == 'register':
                raise ValidationError('用户已存在,请直接登陆')
        else:
            if status == 'login':
                raise ValidationError('用户不存在,请先注册')
        code = sms.get_code()
        # result = sms.send_sms(telephone, code, status)

        # 测试
        print(status)
        print(code)
        result = True
        # 测试完删

        # 验证码保存
        conn = get_redis_connection()
        conn.set(f'{settings.PHONE_CACHE_KEY}{telephone}', code, 180)
        if result:
            return APIResponse(code=1, msg='验证码发送成功')
        else:
            return APIResponse(code=0, msg='验证码发送失败,请稍候重试')


class RegisterView(GenericViewSet, CreateModelMixin):
    queryset = models.User.objects.all()
    serializer_class = serialiser.UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = response.data.get('username')
        return APIResponse(code=1, msg='注册成功', username=username)


