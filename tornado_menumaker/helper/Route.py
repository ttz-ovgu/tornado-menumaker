#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
from functools import partial
import inspect
import re
from types import FunctionType
from tornado.web import URLSpec, Application, RequestHandler

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 23:48'

SUPPORTED_METHODS = RequestHandler.SUPPORTED_METHODS


class Route(URLSpec):
    """
        A route
    """

    def __init__(self, url: str=None, **kwargs):
        super().__init__(url, self, kwargs=kwargs)

        self._url = url
        self._routing = {}

    @property
    def url(self):
        """
            URL of Route (plain without modification)
        """
        return self._url

    @url.setter
    def url(self, pattern: str):
        """
            Set a new url as pattern

            :param pattern: New url value
        """
        self._url = pattern
        if not pattern.endswith('$'):
            pattern += '$'
        self.regex = re.compile(pattern)
        assert len(self.regex.groupindex) in (0, self.regex.groups), \
            ("groups in url regexes must either be all named or all "
             "positional: %r" % self.regex.pattern)
        self._path, self._group_count = self._find_groups()

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            if item.upper() in SUPPORTED_METHODS:
                return partial(self.register, method=item.lower())

    def register(self, function: FunctionType, method: str):
        """
            Register a method function

            :param function: Function to be registered
            :param method: Name of method
        """
        self._routing[method] = function
        return self

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], FunctionType):
            self._routing['get'] = args[0]
            self.__module__ = inspect.getmodule(args[0])
            self.__module__ = args[0].__qualname__.rsplit(".", 3)[-2]
            return self
        elif isinstance(args[0], Application):
            try:
                self.handler = self.cls(*args)
            except AttributeError:
                self.cls = getattr(self.__module__, self.__module__)
                self.handler = self.cls(*args)
            for method, function in self._routing.items():
                setattr(self.handler, method, function.__get__(self.handler))
            return self.handler

    @classmethod
    def isroute(cls, other: object) -> bool:
        """
            Is other an instance of Route?

            :param other: Object to compare
        """
        return isinstance(other, cls)

    @classmethod
    def isindex(cls, other: object) -> bool:
        """
            Is this the index method?

            :param other: Object to compare
        """
        return inspect.isfunction(other) and hasattr(other, '_isindex')

