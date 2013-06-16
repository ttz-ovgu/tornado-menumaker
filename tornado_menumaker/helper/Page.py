#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
import inspect
from tornado.web import RequestHandler, URLSpec

from .Router import Router

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 23:46'


class Page(object):
    """
        A Page
    """

    def __init__(self, handler: RequestHandler, url: str=None, caption: str=None, **kwargs):
        self.handler = handler
        self.url = url
        self.caption = caption
        self.kwargs = kwargs

    @property
    def routes(self):
        urls = set()
        routers = []
        routes = []

        for name, router in inspect.getmembers(self.handler, Router.isinstance):
            routers.append(router)
            urls.update(router.get('url'))

        for url in urls:
            spec = URLSpec(url, self.handler)
            routes.append(spec)
            for router in routers:
                for route in router.find(url=url):
                    route.spec = spec

        return routes
