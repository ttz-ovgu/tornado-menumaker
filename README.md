tornado-menumaker
=================

Inspired by tornroutes a simple menu api

Copyright license
=================

tornado-menumaker is licensed under the GNU Affero General Public License, for more information see the LICENSE.txt.

Usage
=====

Define Handler using decorator:

    import tornado.web
    from tornado_menumaker import page, index, subpage, api

    @page('/news', 'News', icon='icon-news')
    class NewsHandler(tornado.web.RequestHandler):

        @index()
        def get(self):
            pass

        @subpage('/show/(\d+)')
        def get(self, id):
            pass

        @subpage('/new', 'Neue News')
        def get(self):
            pass

        @subpage('/new')
        def post(self):
            pass

        @subpage('/archive', 'Archiv')
        def get(self):
            pass

    a = tornado.web.Application(api.routes())

To get the menu structure you can then use:

    from tornado_menumaker import routes

    for url, caption, sub_routes, kwargs in api.items():
       ...
       for url, caption, subsub_routes, kwargs in sub_routes:
          ...

    This will yield for the above example:
       '/news', 'News', <generator>, {icon: 'icon_news'}
         '/news/new', 'Neue News', <generator>, {}
         '/news/archive', 'Archiv', <generator>, {}







