
from datetime import date
from marketpy.pricer.utils import *
import unittest


class TestUtils(unittest.TestCase):

    def test_simple_exact_noleap(self):
        frac = year_fract(date(2015, 10, 1), date(2015, 12, 15))
        self.assertEqual(round(frac, 6), 0.205479)

    def test_simple_exact_leap(self):
        frac = year_fract(date(2012, 10, 1), date(2012, 12, 15))
        self.assertEqual(round(frac, 6), 0.204918)

    def test_simple_february_noleap(self):
        frac = year_fract(date(2015, 2, 15), date(2015, 3, 15))
        self.assertEqual(round(frac, 6), 0.076712)

    def test_simple_february_leap(self):
        frac = year_fract(date(2016, 2, 15), date(2016, 3, 15))
        self.assertEqual(round(frac, 6), 0.0792350)

    def test_simple_zero(self):
        frac = year_fract(date(2016, 3, 15), date(2016, 2, 15))
        self.assertEqual(round(frac, 6), 0.0)

    def test_half_year_exact(self):
        frac = year_fract(date(2001, 3, 14), date(2001, 9, 14))
        self.assertEqual(round(frac, 4), 0.5041)

    def test_full_year_exact(self):
        frac = year_fract(date(2014, 1, 1), date(2015, 1, 1))
        self.assertEqual(round(frac, 4), 1.0)

    def test_complex_exact_1(self):
        frac = year_fract(date(2014, 7, 27), date(2017, 1, 18))
        self.assertEqual(round(frac, 8), 2.47945205)

    def test_complex_exact_2(self):
        frac = year_fract(date(2012, 7, 27), date(2014, 1, 18))
        self.assertEqual(round(frac, 8), 1.47827682)


if __name__ == '__main__':
    unittest.main()
