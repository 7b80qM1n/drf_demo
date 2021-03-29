from rest_framework.views import exception_handler
from luffyapi.utils.response import APIResponse
from luffyapi.utils.logger import log

def common_exception_handler(exc, context):

    log.error(f'视图{context["view"].__class__.__name__}出错,错误:{str(exc)}')

    ret = exception_handler(exc, context)
    if not ret:
        if isinstance(exc, KeyError):
            return APIResponse(code=0, msg='key error')
        return APIResponse(code=0, msg='error', result=str(exc))
    else:
        return APIResponse(code=0, msg='error', result=ret.data)
