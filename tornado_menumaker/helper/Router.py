#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
from collections import defaultdict
import logging
from types import FunctionType
from tornado.web import RequestHandler, HTTPError

from .Route import Route

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 22:47'


class Router(object):
    """
        A router
    """

    def __init__(self, name: str):
        self.name = name
        self.routes = defaultdict(list)

    def __call__(self, *args, **kwargs):
        logging.warning(args)
        logging.warning(kwargs)

    def __get__(self, obj: RequestHandler, t=None):
        if obj is None:
            return self

        method_name = obj.request.method.lower()
        for route in self.routes[method_name]:
            if route.spec.regex.match(obj.request.path):
                return route.function.__get__(obj, t)
        else:
            raise HTTPError(404, "Could not find route for %s" % obj.request.path)

    def add(self, function: FunctionType, method: str, url: str, caption: str, **kwargs):
        """
            Add a route to this router

            :param function: Function Body
            :param method: Method to listen for
            :param url: Url to be listen for
            :param caption: Caption of the menuitem
            :param kwargs: Additional arguments
        """
        self.routes[method].append(Route(function, url, caption, **kwargs))

    def prepend(self, key: str, value):
        """
            Prepend all route[key]'s with value

            :param key: attribute key
            :param value: value to be prepend
        """
        for routes in self.routes.values():
            for route in routes:
                setattr(route, key, getattr(route, key) is None and value or value + getattr(route, key))

    def get(self, key: str) -> list:
        """
            Get all route[key] values

            :param key: attribute key
        """
        rtn = []
        for routes in self.routes.values():
            for route in routes:
                rtn.append(getattr(route, key))
        return rtn

    def find(self, **kwargs):
        """
            Find all route with key=value for kwargs.items()

            :param kwargs: filter dict to be applied
        """
        rtn = []
        for routes in self.routes.values():
            for route in routes:
                for (key, value) in kwargs.items():
                    if getattr(route, key) != value:
                        break
                else:
                    rtn.append(route)
        return rtn


    @classmethod
    def isinstance(cls, arg):
        """
            Check if arg is instance of ourself

            :param arg:
        """
        return isinstance(arg, cls)
