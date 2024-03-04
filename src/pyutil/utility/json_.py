from json import dumps, load, loads

from pyutil.utility.object import is_basestring, is_dict, is_int, is_list, is_none, is_tuple, is_type_equal, \
    opt_basestring


def parse(str_, fallback=None):
    f = None
    if is_dict(fallback):
        f = fallback

    if is_dict(str_):
        return str_
    elif not is_basestring(str_):
        return f

    try:
        res = loads(str_)
        if is_dict(res):
            return res

        return f

    except:
        return f


def parse_array(str_, fallback=None):
    f = None
    if is_list(fallback):
        f = fallback

    if is_list(str_):
        return str_
    elif not is_basestring(str_):
        return f

    try:
        res = loads(str_)
        if is_list(res):
            return res

        return f

    except:
        return f


def parse_any(str_, fallback=None):
    f = None
    if is_dict(fallback) or is_list(fallback):
        f = fallback

    j = parse(str_)
    if j is None:
        j = parse_array(str_)
        if j is None:
            return f
    return j


def parse_from_file(str_):
    return load(str_)


def _default(obj):
    return '<<non-serializable: {}>>'.format(type(obj).__qualname__)


def stringify(obj):
    return stringify_ignore_non_serializable(obj)


def stringify_compact(obj):
    return dumps(obj, separators=(',', ':'), default=_default)


def stringify_formatted(obj):
    return dumps(obj, indent=2, separators=(',', ': '), default=_default)


def stringify_ignore_non_serializable(obj):
    return dumps(obj, default=_default)


def is_empty(obj):
    if is_dict(obj):
        return not obj
    elif is_list(obj):
        return len(obj) == 0
    else:
        return True


def has(obj, key):
    if is_dict(obj) and is_basestring(key):
        return key in obj
    elif is_list(obj) and is_int(key) and key >= 0:
        return len(obj) > key
    elif is_tuple(obj) and is_int(key) and key >= 0:
        return len(obj) > key
    else:
        return False


def del_(obj, key):
    if has(obj, key):
        del obj[key]


def safe_get(obj, key_input, fallback=None):
    if has(obj, key_input):
        return obj[key_input]

    elif not is_none(obj) and is_list(key_input) and len(key_input) > 0:
        key = key_input[0]
        if len(key_input) == 1:
            return safe_get(obj, key, fallback)

        if has(obj, key):
            return safe_get(obj[key], key_input[1:], fallback)

    return fallback


def safe_deep_get(obj, key_input, fallback=None):
    return safe_get(obj, key_input, fallback)


def safe_get_with_type(obj, key_input, fallback=None):
    if has(obj, key_input):
        value = obj[key_input]
        if not is_none(fallback):
            if not is_type_equal(value, fallback):
                return fallback
        return value

    elif not is_none(obj) and is_list(key_input) and len(key_input) > 0:
        key = key_input[0]
        if len(key_input) == 1:
            return safe_get_with_type(obj, key, fallback)

        if has(obj, key):
            return safe_get_with_type(obj[key], key_input[1:], fallback)

    return fallback


def safe_deep_get_with_type(obj, key_input, fallback=None):
    return safe_get_with_type(obj, key_input, fallback)


def safe_set(obj, key_input, val):
    if is_dict(obj) and is_basestring(key_input):
        if key_input in obj:
            value = obj[key_input]
            if is_type_equal(value, val):
                obj[key_input] = val
        else:
            obj[key_input] = val

    elif is_list(obj) and is_int(key_input) and key_input >= 0:
        if len(obj) > key_input:
            value = obj[key_input]
            if is_type_equal(value, val):
                obj[key_input] = val
        else:
            obj.append(val)

    elif not is_none(obj) and is_list(key_input) and len(key_input) > 0:
        key = key_input[0]
        if len(key_input) == 1:
            safe_set(obj, key, val)
        else:
            if is_dict(obj) and is_basestring(key):
                if key in obj:
                    safe_set(obj[key], key_input[1:], val)
                else:
                    next_key = key_input[1]
                    if is_basestring(next_key):
                        obj[key] = dict()
                        safe_set(obj[key], key_input[1:], val)
                    elif is_int(next_key):
                        obj[key] = list()
                        safe_set(obj[key], key_input[1:], val)
            elif is_list(obj) and is_int(key) and key >= 0:
                if len(obj) > key:
                    safe_set(obj[key], key_input[1:], val)
                else:
                    next_key = key_input[1]
                    if is_basestring(next_key):
                        value = dict()
                        obj.append(value)
                        safe_set(value, key_input[1:], val)
                    elif is_int(next_key):
                        value = list()
                        obj.append(value)
                        safe_set(value, key_input[1:], val)


def safe_deep_set(obj, key_input, val):
    safe_set(obj, key_input, val)


def force_set(obj, key_input, val):
    if is_dict(obj) and is_basestring(key_input):
        obj[key_input] = val

    elif is_list(obj) and is_int(key_input) and key_input >= 0:
        if len(obj) > key_input:
            obj[key_input] = val
        else:
            obj.append(val)

    elif not is_none(obj) and is_list(key_input) and len(key_input) > 0:
        key = key_input[0]
        if len(key_input) == 1:
            force_set(obj, key, val)
        else:
            if is_dict(obj) and is_basestring(key):
                next_key = key_input[1]
                if key in obj:
                    value = obj[key]
                    if is_basestring(next_key):
                        if not is_dict(value):
                            value = dict()
                            obj[key] = value
                        force_set(value, key_input[1:], val)
                    elif is_int(next_key):
                        if not is_list(value):
                            value = list()
                            obj[key] = value
                        force_set(value, key_input[1:], val)
                else:
                    if is_basestring(next_key):
                        obj[key] = dict()
                        force_set(obj[key], key_input[1:], val)
                    elif is_int(next_key):
                        obj[key] = list()
                        force_set(obj[key], key_input[1:], val)
            elif is_list(obj) and is_int(key) and key >= 0:
                next_key = key_input[1]
                if len(obj) > key:
                    value = obj[key]
                    if is_basestring(next_key):
                        if not is_dict(value):
                            value = dict()
                            obj[key] = value
                        force_set(value, key_input[1:], val)
                    elif is_int(next_key):
                        if not is_list(value):
                            value = list()
                            obj[key] = value
                        force_set(value, key_input[1:], val)
                else:
                    if is_basestring(next_key):
                        value = dict()
                        obj.append(value)
                        force_set(value, key_input[1:], val)
                    elif is_int(next_key):
                        value = list()
                        obj.append(value)
                        force_set(value, key_input[1:], val)


def force_deep_set(obj, key_input, val):
    force_set(obj, key_input, val)


def safe_del(obj, key_input):
    if has(obj, key_input):
        del_(obj, key_input)

    elif not is_none(obj) and is_list(key_input) and len(key_input) > 0:
        key = key_input[0]
        if len(key_input) == 1:
            safe_del(obj, key)
        elif has(obj, key):
            safe_del(obj[key], key_input[1:])


def safe_deep_del(obj, key_input):
    safe_del(obj, key_input)


def flatten(obj, delim, parent=None):
    delim = opt_basestring(delim, '.')

    object_ = {}
    _flatten(obj, object_, delim, parent)
    return object_


def _flatten(obj, res, delim, parent):
    if is_dict(obj) or is_list(obj):
        prefix = '' if parent is None else parent + delim
        if is_list(obj):
            for i in range(len(obj)):
                _flatten(obj[i], res, delim, prefix + str(i))
        else:
            for key in obj:
                _flatten(obj[key], res, delim, prefix + key)
    elif is_basestring(parent):
        res[parent] = obj
