#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Annex functions

:version: 0.0
:date: 2016-01-14
:author: Mathieu Voisin
"""

from datetime import date
from calendar import isleap


def year_fract(d1, d2):
    """Return the difference between the dates d1 and d2
    in fractions of years.
    Returns zero for d1 is after of equal to d2.

    :param d1: Value date
    :param d2: Maturity date
    :type d1: datetime.date
    :type d2: datetime.date
    :rtype: float
    """
    if d2.year == d1.year:
        result = max((d2 - d1).days, 0)
        return result / days_in_year(d2.year)
    else:
        result = d2.year - d1.year - 1
        result += (date(d1.year, 12, 31) - d1).days / days_in_year(d1.year)
        result += (d2 - date(d2.year, 1, 1)).days / days_in_year(d2.year)
        return max(result, 0)


def days_in_year(year):
    """Returns the number of days by year.

    :param year: Year ad YYYY format
    :type year: int
    :rtype: int
    """
    if isleap(year):
        return 366
    else:
        return 365
