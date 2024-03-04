# coding=utf-8
"""
Java の CountDownLatch 風なクラス (マルチスレッド処理用)

REFERENCES::
https://stackoverflow.com/questions/10236947/does-python-have-a-similar-control-mechanism-to-javas-countdownlatch
https://qiita.com/shinkiro/items/75f3561d6bc96694ce30
"""
import threading as th


class CountDownLatch:
    """\
    Java の CountDownLatch 風なクラスです。
    使い方は Java 版と同じで以下のメソッドを利用します。

    - count_down
    - await

    ・　count_down メソッドを各プロセスが呼び出しカウントを減らす。
    ・ 待機を行うプロセスは await メソッドで条件が揃うまで待つ。

    本クラスは、スレッド処理で利用できます。

    >>> # ---------------------------------------------
    >>> # スレッド処理で利用する場合
    >>> # ---------------------------------------------
from src import pylatch as pl
    >>> import threading as th
    >>> latch = pl.CountDownLatch(2)
    >>> th1 = th.Thread(target=lambda: latch.count_down())
    >>> th2 = th.Thread(target=lambda: latch.count_down())

    >>> latch.count
    2
    >>> latch.await__(timeout=1.0)
    False

    >>> th1.start()
    >>> th1.join()
    >>> latch.count
    1
    >>> latch.await__(timeout=1.0)
    False

    >>> th2.start()
    >>> th2.join()
    >>> latch.count
    0
    >>> latch.await__(timeout=1.0)
    True
    """

    def __init__(self, count=1):
        """
        オブジェクトを初期化します。

        :param count: カウント。デフォルト値は 1 です。 0 以下は指定できません。(ValueError)
        """
        if count <= 0:
            raise ValueError('0 以下は指定できません。 [' + str(count) + ']')
        self._count = count
        self.lock = th.Condition()

    @property
    def count(self):
        """
        現在のカウントを取得します。

        :return: 現在のカウント
        """
        return self._count

    def count_down(self):
        """
        件数を１減らします。
        """
        with self.lock:
            if self._count > 0:
                self._count -= 1
            if self._count <= 0:
                self.lock.notify_all()

    def await_(self, timeout=None):
        """
        カウントが 0 になるまで待機します。
        timeout を指定している場合、指定時間後に結果を返します。
        戻り値が False の場合、タイムアウトしたことを示します。

        :param timeout: タイムアウト（秒）デフォルトは None で、カウントが 0 になるまで無制限待機します。
        :return: タイムアウトした場合は False。それ以外は True
        """
        with self.lock:
            if self._count > 0:
                return self.lock.wait(timeout=timeout)
            else:
                return True


if __name__ == '__main__':
    import doctest

    doctest.testmod()
