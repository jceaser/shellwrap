from unittest.mock import Mock
from unittest.mock import patch
from unittest.mock import MagicMock

import unittest
import datetime
import shellwrap.datetools as dt

class TestTime(unittest.TestCase):
    """Test suit for date-tools API"""

    def fixed_date_2024_02_14(self):
        return 1707930000

    def fixed_datetime(self):
        return datetime.datetime(2024, 2, 14, 12, 0, 0, 0)

    # **********************************************************************
    # Tests

    def test_now(self):
        dt.now_internal = MagicMock(return_value=self.fixed_datetime())
        self.assertEqual("2024-02-14T12:00:00", dt.now(), "now is broken")

    def test_today(self):
        dt.now_internal = MagicMock(return_value=self.fixed_datetime())
        self.assertEqual("2024-02-14", dt.today(), "today is broken")

    @patch('time.time')
    def test_unix(self, mocked_time_time):
        mocked_time_time.return_value = self.fixed_date_2024_02_14()
        expected = self.fixed_date_2024_02_14()
        actual = dt.unix()
        self.assertEqual(expected, value)

    @patch('time.time')
    def test_unix(self, mocked_time_time):
        mocked_time_time.return_value = self.fixed_date_2024_02_14()

        expected = 1000
        start = self.fixed_date_2024_02_14() - expected
        actual = dt.unix_difference(start)
        self.assertEqual(expected, actual, "date math is wrong")
