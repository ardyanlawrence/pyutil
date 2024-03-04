from socket import timeout as socket_timeout

from httplib import HTTPException, InvalidURL
from urllib2 import HTTPError, URLError, urlopen

from pyutil.result import Result
from pyutil.utility.json_ import parse_any
from pyutil.webservice.wsresult import input_failure, network_failure, timeout as wsresult_timeout, unknown_error


def REQUEST(request, timeout, resp_content_type):
    try:
        response = urlopen(request, timeout=timeout)
        code = response.getcode()

        # Headers
        headers_message = response.info()
        headers = {}
        for header in headers_message.keys():
            header_list = headers_message.getheaders(header)
            if len(header_list) > 1:
                headers[header] = header_list
            else:
                headers[header] = header_list[0]

        # Body
        body = response.read()
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
        headers_message = e.info()
        headers = {}
        for header in headers_message.keys():
            header_list = headers_message.getheaders(header)
            if len(header_list) > 1:
                headers[header] = header_list
            else:
                headers[header] = header_list[0]

        # Body
        body = e.read()
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

    except socket_timeout:
        return wsresult_timeout()

    except URLError as e:
        if e.reason.__str__() == 'timed out':
            return wsresult_timeout()
        else:
            return network_failure()

    except InvalidURL:
        return input_failure()

    except HTTPException:
        return network_failure()

    except:
        pass

    return unknown_error()
