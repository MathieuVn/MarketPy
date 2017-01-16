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

from marketpy.pricer.utils import year_fract


class VanillaOption(object):

    def __init__(self, **kwargs):
        """Vanilla options object.
        Note the you should enter 0.2 for 20% of volatility.

        :paramters:
            - value_date: Date of valuation
            - maturity: Maturity of the option
            - ttm: (optional) Time to maturity in fraction of years
            - type: call (default) or put
            - style: european (default) or american
            - spot: Current spot price of underlying
            - strike: Strike if the option
            - volatility: Implied volatility (annualized) of the underlying
            - r: Interest rate for the maturity
            - div: Annualized dividend yield

        :param kwargs: Parameters describe above
        :type kwargs: dict
        """
        self.value_date = kwargs.get('value_date', date.today())
        self.maturity = kwargs.get(
            'maturity',
            date.today().replace(date.today().year + 1)
        )
        self.ttm = kwargs.get('ttm',
                              year_fract(self.value_date, self.maturity))
        self.option_type = kwargs.get('type', 'call')
        self.option_style = kwargs.get('style', 'european')
        self.K = kwargs.get('strike', 100)
        self.S = kwargs.get('spot', 100)
        self.vol = kwargs.get('volatility', 0.20)
        self.r = kwargs.get('r', 0.05)
        self.q = kwargs.get('div', 0)
        self._a = self.vol * self.ttm ** 0.5
        self._d1 = (log(self.S / self.K) +
                    (self.r - self.q +
                     self.vol ** 2 / 2) * self.ttm) / self._a
        self._d2 = self._d1 - self._a

    def bs_price(self):
        """Black-Scholes-Merton model for pricing european options.

        :rtype: float
        """
        if self.option_style == 'european':
            if self.option_type == 'call':
                return (self.S * exp(- self.q * self.ttm) *
                        norm.cdf(self._d1) - norm.cdf(self._d2) * self.K *
                        exp(- self.r * self.ttm))
            else:
                return (-self.S * exp(- self.q * self.ttm) *
                        norm.cdf(-self._d1) + norm.cdf(-self._d2) *
                        self.K * exp(- self.r * self.ttm))
        else:
            # American options are not supported
            return 0

    def bs_greeks(self):
        """Greeks from Black-Scholes-Merton model for european options.

        :return: dict of greeks [Delta, Gamma, Vega, Theta]
        :rtype: dict
        """
        result = {}
        if self.option_type == 'call':
            result['Delta'] = exp(-self.q * self.ttm) * norm.cdf(self._d1)

            result['Theta1'] = - exp(-self.q * self.ttm) * (
                self.S * norm.pdf(self._d1) * self.vol
            ) / (2 * self.ttm**0.5) - self.r * self.K * exp(
                -self.r * self.ttm
            ) * norm.cdf(self._d2) + self.q * self.S * exp(
                -self.q * self.ttm
            ) * norm.cdf(self._d1)

            result['Theta2'] = 1 / 252 * (
                - ((self.S * self.vol * exp(
                    - self.q * self.ttm
                )) / (2 * self.ttm**0.5) * norm.pdf(self._d1)) -
                self.r * self.K *
                exp(-self.r * self.ttm) * norm.cdf(self._d2) +
                self.q * self.S * exp(
                    - self.q * self.ttm
                ) * norm.cdf(self._d1)
            )

            result['Rho'] = 0.01 * self.K * self.ttm * exp(
                - self.r * self.ttm
            ) * norm.cdf(self._d2)

            result['Charm'] = self.q * exp(-self.q * self.ttm) *\
                norm.cdf(self._d1) - exp(-self.q * self.ttm) *\
                norm.pdf(self._d1) * (
                2 * (self.r - self.q) * self.ttm - self._d2 * self._a
            ) / (2 * self.ttm * self._a)
        elif self.option_type == 'put':
            result['Delta'] = -exp(-self.q * self.ttm) * \
                              norm.cdf(-self._d1)

            result['Theta1'] = - exp(-self.q * self.ttm) * (
                self.S * norm.pdf(self._d1) * self.vol
            ) / (2 * self.ttm**0.5) + self.r * self.K * exp(
                -self.r * self.ttm
            ) * norm.cdf(-self._d2) - self.q * self.S * exp(
                -self.q * self.ttm
            ) * norm.cdf(-self._d1)

            result['Theta2'] = 1 / 252 * (
                - ((self.S * self.vol * exp(
                    - self.q * self.ttm
                )) / (2 * self.ttm ** 0.5) * norm.pdf(self._d1)) + self.r *
                self.K * exp(
                    -self.r * self.ttm
                ) * norm.cdf(-self._d2) - self.q * self.S *
                exp(- self.q * self.ttm) * norm.cdf(-self._d1)
            )

            result['Rho'] = - 0.01 * self.K * self.ttm * exp(
                - self.r * self.ttm
            ) * norm.cdf(-self._d2)

            result['Charm'] = -self.q * exp(-self.q * self.ttm) *\
                norm.cdf(-self._d1) - exp(-self.q * self.ttm) *\
                norm.pdf(self._d1) * (
                2 * (self.r - self.q) * self.ttm - self._d2 * self._a
            ) / (2 * self.ttm * self._a)

        result['Gamma'] = exp(-self.q * self.ttm) / (
            self.S * self.vol * self.ttm ** 0.5
        ) * norm.pdf(self._d1)

        result['Vega'] = 0.01 * self.S * exp(
            -self.q * self.ttm
        ) * self.ttm**0.5 * norm.pdf(self._d1)

        result['Vanna'] = -exp(-self.q * self.ttm) * norm.pdf(self._d1) *\
            self._d2 / self.vol

        result['Vomma'] = result['Vega'] * (self._d1 * self._d2) / self.vol

        result['Speed'] = -result['Gamma'] / self.S * (
            self._d1 / self._a + 1
        )

        result['Zomma'] = result['Gamma'] *\
            (self._d1 * self._d2 - 1) / self.vol

        result['Color'] = -exp(-self.q * self.ttm) * norm.pdf(self._d1) / (
            2 * self.S * self.ttm * self._a
        ) * (2 * self.q * self.ttm + 1 + (
            2 * (self.r - self.q) * self.ttm - self._d2 * self._a
        ) / self._a * self._d1)

        result['Veta'] = self.S * exp(-self.q * self.ttm) *\
            norm.pdf(self._d1) * self.ttm**0.5 * (
            self.q + ((self.r - self.q) * self._d1) / self._a - (
                1 + self._d1 * self._d2
            ) / (2 * self.ttm)
        )

        result['Ultima'] = -result['Vega'] / self.vol**2 * (
            self._d1 * self._d2 * (1 - self._d1 * self._d2) +
            self._d1**2 + self._d2**2
        )
        return result
