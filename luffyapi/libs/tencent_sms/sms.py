from luffyapi.settings import const
from qcloudsms_py import SmsSingleSender
from luffyapi.utils.logger import log
from rest_framework.exceptions import ValidationError
# 生成验证码
def get_code():
    import random
    code = random.randrange(1000, 9999)
    return str(code)

# 发送短信
def send_sms(phone, code, status):
    ssender = SmsSingleSender(const.TENCENT_APPID, const.TENCENT_APPKEY)
    params = [code]
    try:
        sms_id = 0
        if status == 'register':
            sms_id = const.TENCENT_TEMPLATE_ID_Register
        elif status == 'login':
            sms_id = const.TENCENT_TEMPLATE_ID_Login
        else:
            raise ValidationError('参数错误')
        result = ssender.send_with_param(86, phone,
                                         sms_id, params, sign=const.TENCENT_SMS_SIGN, extend="",
                                         ext="")
        if result.get('result') == 0:
            return True
        else:
            return False
    except Exception as e:
        log.error(f'手机号{phone}短信发送失败,原因可能是{e}')
