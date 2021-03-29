from . import models
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from . import serialiser
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from utils.response import APIResponse
from utils.logger import log
from libs.ali_pay import alipay


class PayView(GenericViewSet, CreateModelMixin):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = models.Order.objects.all()
    serializer_class = serialiser.OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.context.get('pay_url'))


class SuccessView(APIView):
    def get(self, request, *args, **kwargs):
        out_trade_no = request.query_params.get('out_trade_no')
        order = models.Order.objects.filter(out_trade_no=out_trade_no).first()
        if order.order_status == 1:
            return APIResponse(code=1, msg='成功')
        else:
            return APIResponse(code=0, msg='付款正在处理,请稍等')

    def post(self, request, *args, **kwargs):
        """支付宝回调接口"""
        data = request.data.dict()
        out_trade_no = data.get('out_trade_no')
        pay_time = data.get('pay_time')
        signature = data.pop('sign')
        success = alipay.verify(data, signature)
        if success and data['trade_status'] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            models.Order.objects.filter(out_trade_no=out_trade_no).update(pay_time=pay_time, order_status=1)
            log.info(f'订单支付成功,订单号:{out_trade_no}')
            return Response('success')
        else:
            log.info(f'订单支付失败,订单号:{out_trade_no}')
            return APIResponse(code=0, msg='失败')
