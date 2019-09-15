__author__ = '星空大师'
__date__ = '2019/7/6 0006 16:07'

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # 首先调用REST框架的默认异常处理程序，
    # 以获得标准的错误响应。
    response = exception_handler(exc, context)
    # 现在将HTTP状态代码添加到响应中。
    if response is not None:
        # response.data.clear()
        response.data['code'] = response.status_code
        response.data['data'] = []

        if response.status_code == 200:
            response.data['success'] = 'ok'

        if response.status_code == 404:
            try:
                response.data['message'] = response.data.pop('detail')
                response.data['message'] = "Not found"
            except KeyError:
                response.data['message'] = "Not found"

        if response.status_code == 400:
            response.data['message'] = 'Input error'

        elif response.status_code == 401:
            response.data['message'] = "Auth failed"

        elif response.status_code >= 500:
            response.data['message'] = "Internal service errors"

        elif response.status_code == 403:
            response.data['message'] = "Access denied"

        elif response.status_code == 405:
            response.data['message'] = 'Request method error'
    return response
