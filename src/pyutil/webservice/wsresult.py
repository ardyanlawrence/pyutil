from pyutil.result import Result


def input_failure():
    return {
        'code': Result.INPUT_FAILURE,
        'text': Result.Message.INPUT_FAILURE
    }


def timeout():
    return {
        'code': Result.TIMEOUT,
        'text': Result.Message.TIMEOUT
    }


def network_failure():
    return {
        'code': Result.NETWORK_FAILURE,
        'text': Result.Message.NETWORK_FAILURE
    }


def unknown_error():
    return {
        'code': Result.UNKNOWN_ERROR,
        'text': Result.Message.UNKNOWN_ERROR
    }
