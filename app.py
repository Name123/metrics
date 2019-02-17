import sys
import os

import tornado.ioloop
import tornado.web
import aiosqlite

from tornado.log import enable_pretty_logging
from tornado.options import define, options

define("db", help="Database path", default="data/records.db")
define("port", help="HTTP Port", default=8989)

import adv.model
from adv.handlers.record import RecordListHandler, RecordCountHandler

def make_app(*args, **kwargs):
    return tornado.web.Application([
        (r"/list", RecordListHandler),
        (r"/count", RecordCountHandler)
    ])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    enable_pretty_logging()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
