from os import mkdir
from shutil import rmtree
from unittest import main, TestCase

from pyutil.utility.file_ import load_config_file, load_yaml_file, merge_config_file, save_config_file


class TestFile(TestCase):

    def test_config(self):

        # Clean up the directory first
        try:
            rmtree('files', True)
        except OSError:
            pass

        # Recreate the directory
        mkdir('files')

        # Object test
        obj = {
            'a': 1,
            'b': 2
        }

        save_config_file(obj, 'files/obj.conf')
        obj2 = load_config_file('files/obj.conf')
        assert obj == obj2

        obj3 = {
            'a': 11,
            'c': 13
        }
        merge_config_file(obj3, 'files/obj.conf')
        obj4 = load_yaml_file('files/obj.conf')
        assert {'a': 11, 'b': 2, 'c': 13} == obj4

        # Array test
        arr = ['a', 'b', 'c']
        save_config_file(arr, 'files/arr.conf')
        arr2 = load_config_file('files/arr.conf')
        assert arr == arr2

        arr3 = ['d', 'e', 'f']
        merge_config_file(arr3, 'files/arr.conf')
        arr4 = load_yaml_file('files/arr.conf')
        assert ['a', 'b', 'c', 'd', 'e', 'f'] == arr4


if __name__ == '__main__':
    main()
