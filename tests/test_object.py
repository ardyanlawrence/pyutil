from unittest import main, TestCase

from pyutil.utility.object import is_basestring, is_int, is_number, is_tuple, is_type_equal, opt_basestring


class TestObject(TestCase):

    def test_is(self):
        assert is_basestring('str')
        assert is_basestring(b'bytes')
        assert is_basestring(u'unicode')
        assert not is_basestring(None)
        assert is_number(1)
        assert is_number(0.1)
        assert not is_number(None)
        assert is_int(1)
        assert not is_int(0.1)
        assert not is_int(None)
        assert is_tuple((1, 2))
        assert not is_tuple(None)
        assert is_type_equal(0, 1)
        assert is_type_equal('s', u's')
        assert is_type_equal(1, 0.1)
        assert is_type_equal(0.5, 5)
        assert not is_type_equal('0.5', 5)

    def test_opt(self):
        obj = None
        assert opt_basestring(obj, 'tests') is not None
        assert not opt_basestring(obj, 5) is not None


if __name__ == '__main__':
    main()
