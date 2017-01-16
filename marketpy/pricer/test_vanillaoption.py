
from datetime import date
from marketpy.pricer.vanillaoption import VanillaOption
import unittest


class TestVanillaOption(unittest.TestCase):

    def test_call_from_hull(self):
        c = VanillaOption(
            type='call',
            spot=42,
            strike=40,
            r=0.1,
            volatility=0.2,
            ttm=0.5
        )
        self.assertEqual(round(c.bs_price(), 2), 4.76)

    def test_put_from_hull(self):
        c = VanillaOption(
            type='put',
            spot=42,
            strike=40,
            r=0.1,
            volatility=0.2,
            ttm=0.5
        )
        self.assertEqual(round(c.bs_price(), 2), 0.81)

    def test_call_struck_atm_low_vol(self):
        c = VanillaOption(
            spot=100,
            strike=100,
            value_date=date(2014, 1, 1),
            maturity=date(2015, 1, 1),
            volatility=0.01,
            r=0.05
        )
        self.assertEqual(round(c.bs_price(), 4), 4.8771)

    def test_call_2(self):
        c = VanillaOption(
            type='call',
            spot=100,
            strike=80,
            value_date=date(2014, 1, 1),
            maturity=date(2015, 1, 1),
            volatility=0.20,
            r=0.05
        )
        self.assertEqual(round(c.bs_price(), 4), 24.5888)

    def test_put_2(self):
        p = VanillaOption(
            type='put',
            spot=100,
            strike=80,
            value_date=date(2014, 1, 1),
            maturity=date(2015, 1, 1),
            volatility=0.20,
            r=0.05
        )
        self.assertEqual(round(p.bs_price(), 4), 0.6872)

    def test_call_with_div(self):
        c = VanillaOption(
            type='call',
            spot=102,
            strike=100,
            value_date=date(2011, 1, 1),
            maturity=date(2013, 1, 1),
            volatility=0.25,
            r=0.05,
            div=0.05
        )
        self.assertEqual(round(c.bs_price(), 4), 13.7480)

    def test_put_with_div(self):
        p = VanillaOption(
            type='put',
            spot=102,
            strike=100,
            value_date=date(2011, 1, 1),
            maturity=date(2013, 1, 1),
            volatility=0.25,
            r=0.05,
            div=0.05
        )
        self.assertEqual(round(p.bs_price(), 4), 11.9384)


if __name__ == '__main__':
    unittest.main()
