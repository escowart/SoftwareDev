import unittest
from evolution.all_evo import *
import time


class TestTimeout(unittest.TestCase):

    def test_time_out_result(self):
        x = 5
        y = self._test_time_out_result(x)
        #self.assertEqual(x, y)

        self.assertRaises(TimeoutDecoratorError, self._test_time_out_result_raise, y)

    @timeout(5)
    def _test_time_out_result(self, a: Any) -> Any:
        return a

    @timeout(1)
    def _test_time_out_result_raise(self, a: Any) -> Any:
        time.sleep(5)
        return a
