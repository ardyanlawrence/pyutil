from pyutil.utility.json_ import safe_del, safe_get
from pyutil.utility.object import is_function


# Context
class Context:

    def __init__(self):
        self.attribute_list = {}
        self.method_list = {}

    def get_attribute(self, key):
        return safe_get(self.attribute_list, [key])

    def put_attribute(self, key, value):
        self.attribute_list[key] = value

    def register_call(self, key, func):
        if is_function(func):
            self.method_list[key] = func

    def unregister_call(self, key):
        safe_del(self.method_list, key)

    def call(self, key, *arg):
        func = safe_get(self.method_list, [key])
        if is_function(func):
            return func(*arg)
