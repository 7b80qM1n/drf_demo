import re
from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError
from django.core.cache import cache
from django_redis import get_redis_connection
from django.conf import settings


# 普通登陆校验
class UserModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['username', 'password', 'id']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        self.context['user'] = user
        self.context['token'] = token

        return attrs

    # 获取用户
    def _get_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        import re
        # 手机校验
        if re.match("^1[3-9][0-9]{9}$", username):
            user = models.User.objects.filter(telephone=username).first()
        # 邮箱校验
        elif re.match("^.+@.+$", username):
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()
        if user:
            ret = user.check_password(password)
            if ret:
                return user
            else:
                raise ValidationError('密码错误')
        else:
            raise ValidationError('用户不存在')

    # 获取token
    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


# 手机验证码登陆校验
class CodeUserSerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['telephone', 'code']

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        self.context['user'] = user
        self.context['token'] = token

        return attrs

    # 获取用户
    def _get_user(self, attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')
        # 取出原来的code
        conn = get_redis_connection()
        cache_code = conn.get(f'{settings.PHONE_CACHE_KEY}{telephone}')
        if code == cache_code:
            # 手机校验
            if re.match("^1[3-9][0-9]{9}$", telephone):
                user = models.User.objects.filter(telephone=telephone).first()
                if user:
                    # 把使用过的验证码删除
                    cache.set(f'{settings.PHONE_CACHE_KEY}{telephone}', '')
                    return user
                else:
                    raise ValidationError('用户不存在,请先注册')
            else:
                raise ValidationError('手机号不合法')
        else:
            raise ValidationError('验证码错误')

    # 获取token
    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


# 注册校验
class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, write_only=True)

    class Meta:
        model = models.User
        fields = ['telephone', 'password', 'code', 'username']
        extra_kwargs = {
            'username': {'read_only': True},
            'password': {'max_length': 18, 'min_length': 12}
        }

    def validate(self, attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')
        conn = get_redis_connection()
        cache_code = conn.get(f'{settings.PHONE_CACHE_KEY}{telephone}')
        if code == cache_code:
            if re.match("^1[3-9][0-9]{9}$", telephone):
                user = models.User.objects.filter(telephone=telephone).first()
                if not user:
                    # 设置用户名
                    attrs['username'] = telephone
                    attrs.pop('code')
                    return attrs
                else:
                    raise ValidationError('该手机号码已注册,请直接登录')
            else:
                raise ValidationError('手机号不合法')
        else:
            raise ValidationError('验证码错误')

    # 重写create
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user
