#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Vanilla Options pricer

:version: 0.0
:date: 2016-01-14
:author: Mathieu Voisin
"""

from datetime import date
from numpy import log, exp
from scipy.stats import norm

from utils import year_fract


class VanillaOption(object):

    def __init__(self, **kwargs):
        self.value_date = kwargs.get('value_date', date.today())
        self.maturity = kwargs.get(
            'maturity',
            date.today().replace(date.today().year + 1)
        )
        self.ttm = year_fract(self.value_date, self.maturity)
        self.option_type = kwargs.get('type', 'call')
        self.option_style = kwargs.get('style', 'european')
        self.strike = kwargs.get('strike', 100)
        self.spot = kwargs.get('spot', 100)
        self.volatility = kwargs.get('volatility', 0.20)
        self.interest_rate = kwargs.get('r', 0.05)
        self.dividend_yield = kwargs.get('div', 0)
        self._a = self.volatility * self.ttm**0.5
        self._d1 = (log(self.spot / self.strike) +
                    (self.interest_rate + self.volatility**2 / 2) * self.ttm /
                    self._a)
        self._d2 = self._d1 - self._a

    def bs_price(self):
        if self.option_style == 'european':
            if self.option_type == 'call':
                return (self.spot * exp(- self.dividend_yield * self.ttm) *
                        norm.cdf(self._d1) - norm.cdf(self._d2) * self.strike *
                        exp(- self.interest_rate * self.ttm))
            else:
                return (-self.spot * exp(- self.dividend_yield * self.ttm) *
                        norm.cdf(-self._d1) + norm.cdf(-self._d2) *
                        self.strike * exp(- self.interest_rate * self.ttm))
        else:
            # American options are not supported
            return 0

    def bs_greeks(self):
        pass
