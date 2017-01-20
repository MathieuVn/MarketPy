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

from marketpy.pricer.utils import year_frac

__all__ = ['VanillaOption']


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
                              year_frac(self.value_date, self.maturity))
        self.option_type = kwargs.get('type', 'call')
        self.option_style = kwargs.get('style', 'european')
        self.K = kwargs.get('strike', 100)
        self.S = kwargs.get('spot', 100)
        self.vol = kwargs.get('volatility', 0.2)
        self.r = kwargs.get('r', 0.05)
        self.q = kwargs.get('div', 0)
        self._update_parameters()

    def set_vol(self, new_vol):
        """Update the volatilty and compute the paramters.

        :param new_vol: New volatility
        :type new_vol: float
        """
        self.vol = new_vol
        self._update_parameters()

    def _update_parameters(self):
        """Update the parameters (d1, d2, etc...).
        """
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

        :List of greeks:

            - Delta
            - Gamma
            - Vega
            - Theta1
            - Theta2
            - Rho
            - Vanna
            - Vomma
            - Charm
            - Speed
            - Zomma
            - Color
            - Veta
            - Ultima

        :return: dict of greeks [Delta, Gamma, Vega, Theta,...]
        :rtype: dict
        """
        result = dict(
            Delta=self._bs_delta(),
            Gamma=self._bs_gamma(),
            Vega=self._bs_vega(),
            Theta1=self._bs_theta1(),
            Theta2=self._bs_theta2(),
            Rho=self._bs_rho(),
            Vanna=self._bs_vanna(),
            Vomma=self._bs_vomma(),
            Charm=self._bs_charm(),
            Speed=self._bs_speed(),
            Zomma=self._bs_zomma(),
            Color=self._bs_color(),
            Veta=self._bs_veta(),
            Ultima=self._bs_ultima()
        )
        return result

    def _bs_delta(self):
        """Compute delta from BSM model.

        :rtype: float or None
        """
        if self.option_type == 'call':
            return exp(-self.q * self.ttm) * norm.cdf(self._d1)
        elif self.option_type == 'put':
            return -exp(-self.q * self.ttm) * norm.cdf(-self._d1)
        else:
            return None

    def _bs_gamma(self):
        """Compute gamma from BSM model.

        :rtype: float
        """
        gamma = exp(-self.q * self.ttm) / (
            self.S * self.vol * self.ttm ** 0.5
        ) * norm.pdf(self._d1)
        return gamma

    def _bs_vega(self):
        """Compute vega from BSM model

        :rtype: float
        """
        vega = 0.01 * self.S * exp(
            -self.q * self.ttm
        ) * self.ttm ** 0.5 * norm.pdf(self._d1)
        return vega

    def _bs_theta1(self):
        """Compute the theta from BSM model.

        :rtype: float or None
        """
        if self.option_type == 'call':
            theta1 = -exp(-self.q * self.ttm) * (
                self.S * norm.pdf(self._d1) * self.vol
            ) / (2 * self.ttm**0.5) - self.r * self.K * exp(
                -self.r * self.ttm
            ) * norm.cdf(self._d2) + self.q * self.S * exp(
                -self.q * self.ttm
            ) * norm.cdf(self._d1)
        elif self.option_type == 'put':
            theta1 = -exp(-self.q * self.ttm) * (
                self.S * norm.pdf(self._d1) * self.vol
            ) / (2 * self.ttm**0.5) + self.r * self.K * exp(
                -self.r * self.ttm
            ) * norm.cdf(-self._d2) - self.q * self.S * exp(
                -self.q * self.ttm
            ) * norm.cdf(-self._d1)
        else:
            theta1 = None
        return theta1

    def _bs_theta2(self, days_period=252):
        """Compute the theta adjusted from BSM model.

        :param days_period: Number of days a period (usually a year)
        :type days_period: int
        :rtype: float or None
        """
        return 1 / days_period * self._bs_theta1()

    def _bs_rho(self):
        """Compute rho from BSM model.

        :rtype: float or None
        """
        if self.option_type == 'call':
            rho = 0.01 * self.K * self.ttm * exp(
                - self.r * self.ttm
            ) * norm.cdf(self._d2)
        elif self.option_type == 'put':
            rho = -0.01 * self.K * self.ttm * exp(
                - self.r * self.ttm
            ) * norm.cdf(-self._d2)
        else:
            rho = None
        return rho

    def _bs_vanna(self):
        """Compute vanna from BSM model.

        :rtype: float
        """
        vanna = -exp(-self.q * self.ttm) * norm.pdf(self._d1) *\
            self._d2 / self.vol
        return vanna

    def _bs_vomma(self):
        """Compute vomma from BSM model.

        :rtype: float
        """
        return self._bs_vega() * (self._d1 * self._d2) / self.vol

    def _bs_charm(self):
        """Compute charm from BSM model.

        :rtype: float or None
        """
        if self.option_type == 'call':
            charm = self.q * exp(-self.q * self.ttm) * \
                norm.cdf(self._d1) - exp(-self.q * self.ttm) * \
                norm.pdf(self._d1) * (
                    2 * (self.r - self.q) * self.ttm - self._d2 * self._a
                ) / (2 * self.ttm * self._a)
        elif self.option_type == 'put':
            charm = -self.q * exp(-self.q * self.ttm) *\
                norm.cdf(-self._d1) - exp(-self.q * self.ttm) *\
                norm.pdf(self._d1) * (
                    2 * (self.r - self.q) * self.ttm - self._d2 * self._a
                ) / (2 * self.ttm * self._a)
        else:
            charm = None
        return charm

    def _bs_speed(self):
        """Compute speed from BSM model.

        :rtype: float
        """
        return -self._bs_gamma() / self.S * (self._d1 / self._a + 1)

    def _bs_zomma(self):
        """Compute zomma from BSM model.

        :rtype: float
        """
        return self._bs_gamma() * (self._d1 * self._d2 - 1) / self.vol

    def _bs_color(self):
        """Compute color from BSM model.

        :rtype: float
        """
        color = -exp(-self.q * self.ttm) * norm.pdf(self._d1) / (
            2 * self.S * self.ttm * self._a
        ) * (2 * self.q * self.ttm + 1 + (
            2 * (self.r - self.q) * self.ttm - self._d2 * self._a
        ) / self._a * self._d1)
        return color

    def _bs_veta(self):
        """Compute veta from BSM model.

        :rtype: float
        """
        veta = self.S * exp(-self.q * self.ttm) *\
            norm.pdf(self._d1) * self.ttm**0.5 * (
            self.q + ((self.r - self.q) * self._d1) / self._a - (
                1 + self._d1 * self._d2
            ) / (2 * self.ttm)
        )
        return veta

    def _bs_ultima(self):
        """Compute ultima from BSM model.

        :rtype: float
        """
        ultima = -self._bs_vega() / self.vol**2 * (
            self._d1 * self._d2 * (1 - self._d1 * self._d2) +
            self._d1**2 + self._d2**2
        )
        return ultima

    def bs_implied_volatility(self, price, bounds=[0, 4], digits=5):
        """

        :param price:
        :param bounds:
        :param digits:
        :return:
        """
        # Save the original volatility
        _vol = self.vol

        # Init
        a = bounds[0]
        b = bounds[1]
        self.set_vol((a + b) / 2)
        count = 0
        cur_price = self.bs_price()

        while round(cur_price, digits) != round(price, digits) and count < 500:
            count += 1
            if cur_price < price:
                a = self.vol
            else:
                b = self.vol
            self.set_vol((a + b) / 2)
            cur_price = self.bs_price()

        implied_vol = self.vol
        self.vol = _vol
        return implied_vol
