from http.client import InvalidURL
from socket import timeout as socket_timeout
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from pyutil.result import Result
from pyutil.utility.json_ import parse_any
from pyutil.webservice.wsresult import input_failure, network_failure, timeout as wsresult_timeout


def REQUEST(request, timeout, resp_content_type):
    try:
        response = urlopen(request, timeout=timeout)
        code = response.getcode()

        # Headers
        headers_message = response.headers
        headers = {}
        for header in headers_message.keys():
            header_list = headers_message.get_all(header)
            if len(header_list) > 1:
                headers[header] = header_list
            else:
                headers[header] = header_list[0]

        # Body
        body = response.read()
        if resp_content_type == 'json' or resp_content_type == 'text':
            content_charset = response.info().get_content_charset('utf-8')
            body = body.decode(content_charset, errors='ignore')
            if resp_content_type == 'json':
                body = parse_any(body)
                if body is None:
                    body = ''

        return {
            'code': code,
            'text': Result.HTTP.Message.get(code),
            'headers': headers,
            'body': body
        }

    except HTTPError as e:
        code = e.getcode()

        # Headers
        headers_message = e.headers
        headers = {}
        for header in headers_message.keys():
            header_list = headers_message.get_all(header)
            if len(header_list) > 1:
                headers[header] = header_list
            else:
                headers[header] = header_list[0]

        # Body
        body = e.read()
        if resp_content_type == 'json' or resp_content_type == 'text':
            content_charset = e.info().get_content_charset('utf-8')
            body = body.decode(content_charset, errors='ignore')
            if resp_content_type == 'json':
                body = parse_any(body)
                if body is None:
                    body = ''

        return {
            'code': code,
            'text': Result.HTTP.Message.get(code),
            'headers': headers,
            'body': body
        }

    except InvalidURL:
        return input_failure()

    except socket_timeout:
        return wsresult_timeout()

    except URLError as e:
        if e.reason.__str__() == 'timed out':
            return wsresult_timeout()
        else:
            return network_failure()

    except:
        pass

    return network_failure()
