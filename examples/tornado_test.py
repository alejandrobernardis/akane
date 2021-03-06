#!/usr/bin/env python

import uuid

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen

from akane import Client


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class OverviewHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        data = yield [
            gen.Task(self.db.set, 'k_1', '1'),
            gen.Task(self.db.set, 'k_2', '55'),
            gen.Task(self.db.get, 'k_1'),
            gen.Task(self.db.getset, 'k_1', '5'),
            gen.Task(self.db.get, 'k_1'),
            gen.Task(self.db.mset, {'k_2': '22', 'k_3': '33'}),
            gen.Task(self.db.get, 'k_2'),
            gen.Task(self.db.mget, ('k_2', 'k_3')),
        ]
        for d in data:
            self.write('%r<br>' % d)

        data = yield gen.Task(self.db.decr, 'k_1')
        self.write('%r<br>' % data)
        data = yield gen.Task(self.db.mset, {'k_2': '22', 'k_3': '33'})
        self.write('%r<br>' % data)
        data = yield gen.Task(self.db.mget, ('k_2', 'k_3'))
        self.write('%r<br>' % data)

        d1 = yield gen.Task(self.db.set, 'k_1', '123')
        d2 = yield gen.Task(self.db.get, 'k_1')
        self.write('%r - %r<br>' % (d1, d2))

        self.write('Hashes:<br><br>')

        d1 = yield gen.Task(self.db.hset, 'hash_key', 'hash_field', 'hash_value')
        d2 = yield gen.Task(self.db.hget, 'hash_key', 'hash_field')
        self.write('%r - %r<br>' % (d1, d2))
        d1 = yield gen.Task(self.db.hset, 'hash_key', 'some_field', 'some_value')
        d2 = yield gen.Task(self.db.hget, 'hash_key', 'some_field')
        self.write('%r - %r<br>' % (d1, d2))

        data = yield gen.Task(self.db.hgetall, 'hash_key')
        self.write('%r<br>' % (data,))

        self.finish()


if __name__ == '__main__':
    try:
        tornado.options.parse_command_line()

        application = tornado.web.Application((
            (r'/', OverviewHandler),
        ), debug=True)
        application.db = Client({
            'connections': 10
        })

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('Exit')
