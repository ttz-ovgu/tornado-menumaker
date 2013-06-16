#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
from types import FunctionType

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 23:48'


class Route(object):
    """
        A route
    """

    def __init__(self, function: FunctionType, url: str=None, caption: str=None, **kwargs):
        self.function = function
        self.url = url
        self.caption = caption
        self.kwargs = kwargs
        self.spec = None