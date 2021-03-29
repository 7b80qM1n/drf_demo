from rest_framework import serializers
from course.models import Course
from . import models
from rest_framework.exceptions import ValidationError


class OrderSerializer(serializers.ModelSerializer):
    # 前端course[1,2,3] ==后端处理==> course[obj1,obj2,obj3]
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, many=True)

    class Meta:
        model = models.Order
        fields = ['subject', 'total_amount', 'pay_type', 'course']
        extra_kwargs = {
            'pay_type': {'required': True, 'help_text': '支付的类型'},
            'total_amount': {'required': True, 'help_text': '商品总金额'}
        }

    def _check_price(self, attrs):
        total_amount = attrs.get('total_amount')
        course_list = attrs.get('course')
        total_price = 0
        for course in course_list:
            total_price += course.price
        if total_amount != total_price:
            print(total_amount)
            print(total_price)
            raise ValidationError('价格不合法')
        return total_amount

    def _get_out_trade_no(self):
        import uuid
        return str(uuid.uuid4())

    def _get_user(self):
        request = self.context.get('request')
        return request.user

    def _get_pay_url(self, out_trade_no, total_amount, subject):
        from libs.ali_pay import alipay, gateway
        from django.conf import settings
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=out_trade_no,
            total_amount=float(total_amount),
            subject=subject,
            return_url=settings.RETURN_URL,
            notify_url=settings.NOTIFY_URL  # 可选, 不填则使用默认notify url
        )
        return gateway + order_string

    def _before_create(self, attrs, user, out_trade_no, pay_url):
        attrs['user'] = user
        attrs['out_trade_no'] = out_trade_no
        self.context['pay_url'] = pay_url

    def validate(self, attrs):
        # 订单总价格校验
        total_amount = self._check_price(attrs)
        # 生成订单号
        out_trade_no = self._get_out_trade_no()
        # 支付的用户
        user = self._get_user()
        # 支付连接生成
        pay_url = self._get_pay_url(out_trade_no, total_amount, subject=attrs.get('subject'))
        # 入库准备(把用户放入)
        self._before_create(attrs, user, out_trade_no, pay_url)
        return attrs

    # 入库
    def create(self, validated_data):
        course_list = validated_data.pop('course')
        order = models.Order.objects.create(**validated_data)
        for course in course_list:
            models.OrderDetail.objects.create(order=order, course=course, price=course.price, real_price=course.price)
        return order
