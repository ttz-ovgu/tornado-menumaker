#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
import inspect
from types import FunctionType
from tornado.web import RequestHandler

from .helper.Router import Router
from .helper.Page import Page

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 22:16'


class ApiManager(object):
    def __init__(self):

        self._router = {}
        self._pages = []

    def add_page(self, handler: RequestHandler, url: str, caption: str, **kwargs):

        # Prefix all urls
        routers = set()
        for name, router in inspect.getmembers(handler, Router.isinstance):
            routers.add(router)
        for router in routers:
            router.prepend('url', url)

        # Register page
        self._pages.append(Page(handler, caption, **kwargs))

    def add_route(self, function: FunctionType, url: str, caption: str, **kwargs) -> Router:

        # Resolve name
        module_name = function.__module__
        handler_name, function_name = function.__qualname__.rsplit('.', 1)
        router_name = "%s.%s" % (module_name, handler_name)

        # Add generic router
        if not router_name in self._router:
            router = self._router[router_name] = Router(router_name)
        else:
            router = self._router[router_name]

        # Add route
        router.add(function=function, method=function_name, url=url, caption=caption, **kwargs)

        # Return router
        return router

    def routes(self):
        """
            Get all routes
        """
        rtn = []

        for page in self._pages:
            rtn.extend(page.routes)

        return rtn

