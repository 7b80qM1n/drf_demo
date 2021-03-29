from alipay import AliPay
from django.conf import settings

alipay = AliPay(
    appid=settings.ALIPAY_APPID,
    app_notify_url=None,  # 默认回调url
    app_private_key_string=settings.APP_PRIVATE_KEY_STRING,  # 应用私钥
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,  # 支付宝公钥
    sign_type=settings.SIGN_TYPE,  # RSA 或者 RSA2
    debug=settings.DEBUG,
    )  # 默认False

gateway = settings.GATEWAY

# subject = "韩红版充气娃娃"
#
# # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
# order_string = alipay.api_alipay_trade_page_pay(
#     out_trade_no="201611121212424",
#     total_amount=10000,
#     subject=subject,
#     return_url="https://www.baidu.com",
#     notify_url="https://www.baidu.com/notify"  # 可选, 不填则使用默认notify url
# )
#
# print(settings.GATEWAY + f'{order_string}')
