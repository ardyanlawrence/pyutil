from ruamel.yaml import StringIO, YAML

from pyutil.utility.json_ import is_empty, parse, parse_any, stringify_formatted
from pyutil.utility.object import is_basestring, is_dict, is_list


def load_config_file(path):
    obj = load_yaml_file(path)
    if obj is None:
        return load_json_file(path)
    return obj


def save_config_file(json, path):
    return save_yaml_file(json, path)


def merge_config_file(json, path):
    if not is_basestring(path):
        return False

    if is_dict(json):
        is_input_dict = True
    elif is_list(json):
        is_input_dict = False
    else:
        return False

    res = False
    file_ = None
    try:
        file_ = open(path, 'r+')
        yaml = YAML(typ='safe')
        obj = yaml.load(file_)
        if obj is None:
            data = file_.read()
            obj = parse_any(data)

        if is_input_dict:
            # Dict
            if is_dict(obj):
                obj.update(json)
            else:
                obj = json
            file_.truncate(0)
            file_.seek(0)
            if is_empty(obj):
                file_.write('')
            else:
                yaml = YAML()
                yaml.indent(mapping=2, sequence=4, offset=2)
                file_.write(_json_to_yaml_str(obj))
            file_.flush()
            res = True

        else:
            # List
            if is_list(obj):
                obj.extend(json)
            else:
                obj = json
            file_.truncate(0)
            file_.seek(0)
            if is_empty(obj):
                file_.write('')
            else:
                yaml = YAML()
                yaml.indent(mapping=2, sequence=4, offset=2)
                file_.write(_json_to_yaml_str(obj))
            file_.flush()
            res = True

    except IOError:
        try:
            file_ = open(path, 'w')
            if is_empty(json):
                file_.write('')
            else:
                yaml = YAML()
                yaml.indent(mapping=2, sequence=4, offset=2)
                file_.write(_json_to_yaml_str(json))
            file_.flush()
            res = True

        except IOError:
            pass

    if file_ is not None:
        file_.close()

    return res


def load_json_file(path):
    if not is_basestring(path):
        return None

    file_ = None
    try:
        file_ = open(path, 'r')
        data = file_.read()
        obj = parse(data)
    except IOError:
        obj = None

    if file_ is not None:
        file_.close()

    return obj


def save_json_file(json, path):
    if not is_basestring(path) or not (is_dict(json) or is_list(json)):
        return False

    res = False
    file_ = None
    try:
        file_ = open(path, 'w')
        if is_empty(json):
            file_.write('')
        else:
            file_.write(stringify_formatted(json))
        file_.flush()
        res = True

    except IOError:
        pass

    if file_ is not None:
        file_.close()

    return res


def merge_json_file(json, path):
    if not is_basestring(path):
        return False

    if is_dict(json):
        is_input_dict = True
    elif is_list(json):
        is_input_dict = False
    else:
        return False

    res = False
    file_ = None
    try:
        file_ = open(path, 'r+')
        data = file_.read()
        obj = parse_any(data)

        if is_input_dict:
            # Dict
            if is_dict(obj):
                obj.update(json)
            else:
                obj = json
            file_.truncate(0)
            file_.seek(0)
            if is_empty(obj):
                file_.write('')
            else:
                file_.write(stringify_formatted(obj))
            file_.flush()
            res = True

        else:
            # List
            if is_list(obj):
                obj.extend(json)
            else:
                obj = json
            file_.truncate(0)
            file_.seek(0)
            if is_empty(obj):
                file_.write('')
            else:
                file_.write(stringify_formatted(obj))
            file_.flush()
            res = True

    except IOError:
        try:
            file_ = open(path, 'w')
            if is_empty(json):
                file_.write('')
            else:
                file_.write(stringify_formatted(json))
            file_.flush()
            res = True

        except IOError:
            pass

    if file_ is not None:
        file_.close()

    return res


def load_yaml_file(path):
    if not is_basestring(path):
        return None

    file_ = None
    try:
        file_ = open(path, 'r')
        yaml = YAML(typ='safe')
        obj = yaml.load(file_)
    except IOError:
        obj = None

    if file_ is not None:
        file_.close()

    return obj


def save_yaml_file(json, path):
    if not is_basestring(path) or not (is_dict(json) or is_list(json)):
        return False

    res = False
    file_ = None
    try:
        file_ = open(path, 'w')
        if is_empty(json):
            file_.write('')
        else:
            yaml = YAML()
            yaml.indent(mapping=2, sequence=4, offset=2)
            file_.write(_json_to_yaml_str(json))
        file_.flush()
        res = True

    except IOError:
        pass

    if file_ is not None:
        file_.close()

    return res


def merge_yaml_file(json, path):
    if not is_basestring(path):
        return False

    if is_dict(json):
        is_input_dict = True
    elif is_list(json):
        is_input_dict = False
    else:
        return False

    res = False
    file_ = None
    try:
        file_ = open(path, 'r+')
        yaml = YAML(typ='safe')
        obj = yaml.load(file_)

        if is_input_dict:
            # Dict
            if is_dict(obj):
                obj.update(json)
            else:
                obj = json
            file_.truncate(0)
            file_.seek(0)
            if is_empty(obj):
                file_.write('')
            else:
                yaml = YAML()
                yaml.indent(mapping=2, sequence=4, offset=2)
                file_.write(_json_to_yaml_str(obj))
            file_.flush()
            res = True

        else:
            # List
            if is_list(obj):
                obj.extend(json)
            else:
                obj = json
            file_.truncate(0)
            file_.seek(0)
            if is_empty(obj):
                file_.write('')
            else:
                yaml = YAML()
                yaml.indent(mapping=2, sequence=4, offset=2)
                file_.write(_json_to_yaml_str(obj))
            file_.flush()
            res = True

    except IOError:
        try:
            file_ = open(path, 'w')
            if is_empty(json):
                file_.write('')
            else:
                yaml = YAML()
                yaml.indent(mapping=2, sequence=4, offset=2)
                file_.write(_json_to_yaml_str(json))
            file_.flush()
            res = True

        except IOError:
            pass

    if file_ is not None:
        file_.close()

    return res


def _json_to_yaml_str(json):
    yaml = YAML()
    stream = StringIO()
    yaml.dump(json, stream, **{})
    result = stream.getvalue()
    stream.close()
    return result
