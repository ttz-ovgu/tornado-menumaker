#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
import inspect
from nose.pyversion import ClassType
from tornado.web import URLSpec, Application

from .Route import Route

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 23:46'


class Page(URLSpec):
    """
        A Page
    """

    def __init__(self, url: str=None, caption: str=None, **kwargs):
        super().__init__(url, self, kwargs=kwargs)

        self._caption = caption
        self._url = url
        self._index = None

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], Application):
            self.handler = self.cls(*args)

            if self._index is not None:
                self.handler.get = self._index.__get__(self.handler)

            return self.handler
        elif isinstance(args[0], ClassType):
            self.cls = args[0]

            for n, route in inspect.getmembers(self.cls, Route.isroute):
                route.url = self._url + route.url
                route.cls = self.cls

            for n, method in inspect.getmembers(self.cls, Route.isindex):
                self._index = method

            return self