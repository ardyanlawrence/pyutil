# coding=utf-8
"""
pylatch.processlatch のユニットテストが定義されています。

REFERENCES::
http://d.hatena.ne.jp/pythonco/20061015/p3
https://www.yoheim.net/blog.php?q=20160903
https://docs.python.jp/3/library/doctest.html
"""
import unittest as ut
#import doctest as dc
import pylatch.processlatch as pl


class TestCountDownLatch(ut.TestCase):
    """pylatch.processlatch.CountDownLatch のユニットテストクラスです。"""

    def test_doctest(self):
        """doctest を実行します。"""
        #ut.TextTestRunner().run(dc.DocTestSuite(pl))

    def test_ctor_nagative_count(self):
        """ctor に負のカウントを指定した場合に例外が発生することを確認します。"""
        # arrange
        # act
        # assert
        with self.assertRaises(ValueError):
            pl.CountDownLatch(-1)

    def test_count_should_not_be_negative(self):
        """count_downを繰り返してもcountは0より小さくはならないことを確認します。"""
        # arrange
        sut = pl.CountDownLatch(2)

        # act
        for i in range(10):
            sut.count_down()

        # assert
        self.assertEqual(0, sut.count)