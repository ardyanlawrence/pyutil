from unittest import main, TestCase

from pyutil.utility.json_ import flatten, force_set, is_empty, parse, parse_any, parse_array, safe_del, safe_get, \
    safe_set
from pyutil.utility.object import is_dict, is_list


class TestJson(TestCase):

    def test_json_empty(self):
        obj = {}
        assert is_empty(obj) is True
        arr = []
        assert is_empty(arr) is True

    def test_json_parse(self):
        obj = parse('{"a": "b"}')
        assert is_dict(obj)
        arr = parse_array('[1,2,3]')
        assert is_list(arr)
        any_ = parse_any('{"a": "b"}')
        assert is_dict(any_)
        any_ = parse_any('[1,2,3]')
        assert is_list(any_)

    def test_json_deep(self):
        # Test deep
        obj = dict()
        safe_set(obj, ['a', 0, 'c', 'e'], 100)
        assert obj == {'a': [{'c': {'e': 100}}]}
        force_set(obj, ['a', 0, 'c', 'd', '3', 3], 5000)
        assert obj == {'a': [{'c': {'e': 100, 'd': {'3': [5000]}}}]}
        assert safe_get(obj, 'a') == [{'c': {'e': 100, 'd': {'3': [5000]}}}]
        safe_del(obj, ['a', 0])
        assert obj == {'a': []}

        # Test basestring
        obj2 = dict()
        safe_set(obj2, 'a', 'a')
        assert obj2 == {'a': 'a'}
        safe_set(obj2, 'a', u'a')
        assert obj2 == {'a': u'a'}
        safe_set(obj2, 'a', 'b')
        assert obj2 == {'a': 'b'}

        # Test tuple
        obj3 = dict()
        safe_set(obj3, 'tuple', ('a', {'b': 10}))
        assert safe_get(obj3, ['tuple', 0]) == 'a'
        assert safe_get(obj3, ['tuple', 1, 'b']) == 10

    def test_json_flatten(self):
        obj = flatten([{'1': 2}, '2', 'alpha', {'oslo': {'zulu': 26}}], '.')
        assert safe_get(obj, '0.1') == 2
        assert safe_get(obj, '1') == '2'
        assert safe_get(obj, '2') == 'alpha'
        assert safe_get(obj, '3.oslo.zulu') == 26

        obj2 = flatten({
            'abc': {
                'def': {
                    'ghi': 'jkl'
                }
            },
            'def': {
                '1': 2
            },
            'ghi': '2',
            'jkl': 'alpha',
            'mno': {
                'oslo': {
                    'zulu': 26
                }
            }
        }, '.')
        assert safe_get(obj2, 'abc.def.ghi') == 'jkl'
        assert safe_get(obj2, 'def.1') == 2
        assert safe_get(obj2, 'ghi') == '2'
        assert safe_get(obj2, 'jkl') == 'alpha'
        assert safe_get(obj2, 'mno.oslo.zulu') == 26


if __name__ == '__main__':
    main()
