
from datetime import date
from utils import *
import unittest


class TestUtils(unittest.TestCase):

    def year_frac_1(self):
        frac = year_fract(date(2015, 10, 1), date(2015, 12, 15))
        self.assertEqual(round(frac, 6), 0.205479)


if __name__ == '__main__':
    unittest.main()
