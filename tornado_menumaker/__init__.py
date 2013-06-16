#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
from types import FunctionType
from tornado.web import RequestHandler

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 21:45'

# Create ApiManager
from .ApiManager import ApiManager

api = ApiManager()


def page(url: str, caption: str, **kwargs):
    """
        Decorate a handler to act as a menumaker page

        :param url: Prefix for all routes of this handler
        :param caption: Caption of the page
        :param kwargs: Additional arguments
    """

    def page_decorator(handler: RequestHandler):
        """
            Decorator for tornado_menumaker.page

            :param handler: RequestHandler
        """
        page = api.add_page(handler=handler, url=url, caption=caption, **kwargs)
        handler._torn_page = page
        return handler

    return page_decorator


def index(url: str=None, caption: str=None, **kwargs):
    """
        Route for index of page

        :param url: Alternative suburl to be registered (otherwise page.url will be used)
        :param caption: Caption of the menu item (if omitted page.caption is used)
        :param kwargs: Additional arguments
    """

    def index_decorator(function: FunctionType):
        """
            Decorator for tornado_menumaker.index

            :param function: Function
        """
        router = api.add_route(function=function, url=url, caption=caption, **kwargs)
        return router

    return index_decorator


def subpage(url: str, caption: str=None, **kwargs):
    """
        Route for a subpage

        :param url: Url of this subpage (will be prefixed with page.url)
        :param caption: Caption of the menu item (if omitted only route will be created)
        :param kwargs: Additional arguments
    """

    def subpage_decorator(function: FunctionType):
        """
            Decorator for tornado_menumaker.subpage

            :param function: Function
        """
        router = api.add_route(function=function, url=url, caption=caption, **kwargs)
        return router

    return subpage_decorator


def subsubpage(url: str, caption: str=None, **kwargs):
    """
        Route for a subpage of a subpage

        :param url: Url of this subpage (will be prefixed with page.url), must be prefixed with the url of the subpage
        :param caption: Caption of the menu item (if omitted only route will be created)
        :param kwargs: Additional arguments
    """

    def subpage_decorator(function: FunctionType):
        """
            Decorator for tornado_menumaker.subpage

            :param function: Function
        """
        router = api.add_route(function=function, url=url, caption=caption, **kwargs)
        return router

    return subpage_decorator