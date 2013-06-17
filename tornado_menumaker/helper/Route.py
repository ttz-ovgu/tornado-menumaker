#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
import inspect
import re
from types import FunctionType
from tornado.web import URLSpec, Application

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 23:48'


class Route(URLSpec):
    """
        A route
    """

    def __init__(self, url: str=None, **kwargs):
        super().__init__(url, self, kwargs=kwargs)

        self._url = url

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

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], FunctionType):
            self.function = args[0]
            return self
        elif isinstance(args[0], Application):
            try:
                self.handler = self.cls(*args)
            except AttributeError:
                module = inspect.getmodule(self.function)
                cls_name = self.function.__qualname__.rsplit(".", 3)[-2]
                self.cls = getattr(module, cls_name)
                self.handler = self.cls(*args)
            self.handler.get = self.function.__get__(self.handler)
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

