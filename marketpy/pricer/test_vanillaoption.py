
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
        self.assertEqual(round(c.bs_price(), 5), 13.74804)

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
        self.assertEqual(round(p.bs_price(), 5), 11.93836)

    def test_first_order_greeks_call(self):
        c = VanillaOption(
            type='call',
            spot=102,
            strike=100,
            value_date=date(2013, 1, 1),
            maturity=date(2014, 1, 1),
            volatility=0.25,
            r=0.05
        )
        res = dict(
            Delta=0.65697,
            Gamma=0.01442,
            Theta1=-7.35702,
            Theta2=-0.02919,
            Vega=0.37500,
            Rho=0.53390
        )
        self.assertEqual(
            {k: round(v, 5) for k, v in c.bs_greeks().items()
             if k in res.keys()},
            res
        )

    def test_first_order_greeks_put(self):
        c = VanillaOption(
            type='put',
            spot=102,
            strike=100,
            value_date=date(2013, 1, 1),
            maturity=date(2014, 1, 1),
            volatility=0.25,
            r=0.05
        )
        res = dict(
            Delta=-0.34303,
            Gamma=0.01442,
            Theta1=-2.60088,
            Theta2=-0.01032,
            Vega=0.37500,
            Rho=-0.41733
        )
        self.assertEqual(
            {k: round(v, 5) for k, v in c.bs_greeks().items()
             if k in res.keys()},
            res
        )


if __name__ == '__main__':
    unittest.main()
