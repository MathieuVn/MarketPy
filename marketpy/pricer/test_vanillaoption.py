
from datetime import date
from vanillaoption import VanillaOption
import unittest


class TestVanillaOption(unittest.TestCase):

    def test_call_1(self):
        c = VanillaOption(
            spot=100,
            strike=100,
            value_date=date(2014, 1, 1),
            maturity=date(2015, 1, 1),
            volatility=0.01,
            interest_rate=0.05
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
            interest_rate=0.05
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
            interest_rate=0.05
        )
        self.assertEqual(round(p.bs_price(), 4), 0.6872)


if __name__ == '__main__':
    unittest.main()
