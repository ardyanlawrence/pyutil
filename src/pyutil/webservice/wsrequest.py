from sys import version_info

from pyutil.utility.bytes_ import from_basestring, is_bytes
from pyutil.utility.json_ import del_, stringify
from pyutil.utility.object import is_basestring, is_dict, is_list, opt_basestring, opt_int
from pyutil.webservice.wsresult import input_failure

TIMEOUT = 10


def __is_python_3():
    major = version_info[0]
    return major == 3


if __is_python_3():
    from urllib.parse import urlencode as urlencode_3
    from urllib.request import Request as Request_3
    from pyutil.webservice.__wsrequest_3 import REQUEST as REQUEST_3

    __urlencode = urlencode_3


    def __Request(url, method, headers, data):
        return Request_3(url, method=method, headers=headers, data=data)


    __REQUEST = REQUEST_3

else:
    from urllib import urlencode as urlencode_2
    from urllib2 import Request as Request_2
    from pyutil.webservice.__wsrequest_2 import REQUEST as REQUEST_2

    __urlencode = urlencode_2


    def __Request(url, method, headers, data):
        return Request_2(url, headers=headers, data=data)


    __REQUEST = REQUEST_2


def request_without_body(url, method=None, query_params=None, headers=None, timeout=None,
                         resp_content_type=None):
    if not is_basestring(url):
        return input_failure()

    method = opt_basestring(method, 'GET')
    timeout = opt_int(timeout, TIMEOUT)
    resp_content_type = opt_basestring(resp_content_type, 'bytes')

    option_query_params = ''
    if is_dict(query_params):
        option_query_params = '?' + __urlencode(query_params, True)
    url += option_query_params

    option_headers = {}
    if is_dict(headers):
        option_headers = headers

    request = __Request(url, method=method, headers=option_headers, data=None)
    return __REQUEST(request, timeout, resp_content_type)


def request_with_body(url, method=None, query_params=None, headers=None, body=None, timeout=None,
                      resp_content_type=None):
    if not is_basestring(url):
        return input_failure()

    method = opt_basestring(method, 'POST')
    timeout = opt_int(timeout, TIMEOUT)
    resp_content_type = opt_basestring(resp_content_type, 'bytes')

    option_query_params = ''
    if is_dict(query_params):
        option_query_params = '?' + __urlencode(query_params, True)
    url += option_query_params

    option_headers = {}
    if is_dict(headers):
        option_headers = headers

    if is_dict(body) or is_list(body):
        if 'Content-Type' not in option_headers:
            option_headers['Content-Type'] = 'application/json'
        elif '' == option_headers['Content-Type']:
            del_(option_headers, 'Content-Type')
        option_body = stringify(body)
    elif is_basestring(body):
        if 'Content-Type' not in option_headers:
            option_headers['Content-Type'] = 'text/plain'
        elif '' == option_headers['Content-Type']:
            del_(option_headers, 'Content-Type')
        option_body = body
    elif is_bytes(body):
        if 'Content-Type' not in option_headers:
            option_headers['Content-Type'] = 'application/octet-stream'
        elif '' == option_headers['Content-Type']:
            del_(option_headers, 'Content-Type')
        option_body = body
    elif body is None:
        option_body = ''
    else:
        option_body = str(body)

    if not is_bytes(option_body):
        option_body = from_basestring(option_body)

    request = __Request(url, method=method, headers=option_headers, data=option_body)
    return __REQUEST(request, timeout, resp_content_type)


def GET(url, query_params=None, headers=None, timeout=None, resp_content_type=None):
    return request_without_body(url, 'GET', query_params, headers, timeout, resp_content_type)


def POST(url, query_params=None, headers=None, body=None, timeout=None, resp_content_type=None):
    return request_with_body(url, 'POST', query_params, headers, body, timeout, resp_content_type)


def PUT(url, query_params=None, headers=None, body=None, timeout=None, resp_content_type=None):
    return request_with_body(url, 'PUT', query_params, headers, body, timeout, resp_content_type)


def DELETE(url, query_params=None, headers=None, timeout=None, resp_content_type=None):
    return request_without_body(url, 'DELETE', query_params, headers, timeout, resp_content_type)


def PATCH(url, query_params=None, headers=None, body=None, timeout=None, resp_content_type=None):
    return request_with_body(url, 'PATCH', query_params, headers, body, timeout, resp_content_type)


def TGET(url, query_params=None, headers=None, timeout=None):
    return GET(url, query_params, headers, timeout, 'text')


def JGET(url, query_params=None, headers=None, timeout=None):
    return GET(url, query_params, headers, timeout, 'json')


def BGET(url, query_params=None, headers=None, timeout=None):
    return GET(url, query_params, headers, timeout, 'bytes')


def TPOST(url, query_params=None, headers=None, body=None, timeout=None):
    if body is not None and not is_basestring(body):
        return input_failure()
    return POST(url, query_params, headers, body, timeout, 'text')


def JPOST(url, query_params=None, headers=None, body=None, timeout=None):
    if body is not None and not is_dict(body) and not is_list(body):
        return input_failure()
    return POST(url, query_params, headers, body, timeout, 'json')


def BPOST(url, query_params=None, headers=None, body=None, timeout=None):
    if body is not None and not is_bytes(body):
        return input_failure()
    return POST(url, query_params, headers, body, timeout, 'bytes')


def TPUT(url, query_params=None, headers=None, body=None, timeout=None):
    if body is not None and not is_basestring(body):
        return input_failure()
    return PUT(url, query_params, headers, body, timeout, 'text')


def JPUT(url, query_params=None, headers=None, body=None, timeout=None):
    if body is not None and not is_dict(body) and not is_list(body):
        return input_failure()
    return PUT(url, query_params, headers, body, timeout, 'json')


def BPUT(url, query_params=None, headers=None, body=None, timeout=None):
    if body is not None and not is_bytes(body):
        return input_failure()
    return PUT(url, query_params, headers, body, timeout, 'bytes')


def TDELETE(url, query_params=None, headers=None, timeout=None):
    return DELETE(url, query_params, headers, timeout, 'text')


def JDELETE(url, query_params=None, headers=None, timeout=None):
    return DELETE(url, query_params, headers, timeout, 'json')


def BDELETE(url, query_params=None, headers=None, timeout=None):
    return DELETE(url, query_params, headers, timeout, 'bytes')


def TPATCH(url, query_params=None, headers=None, body=None, timeout=None):
    if body is not None and not is_basestring(body):
        return input_failure()
    return PATCH(url, query_params, headers, body, timeout, 'text')


def JPATCH(url, query_params=None, headers=None, body=None, timeout=None):
    if body is not None and not is_dict(body) and not is_list(body):
        return input_failure()
    return PATCH(url, query_params, headers, body, timeout, 'json')


def BPATCH(url, query_params=None, headers=None, body=None, timeout=None):
    if body is not None and not is_bytes(body):
        return input_failure()
    return PATCH(url, query_params, headers, body, timeout, 'bytes')
