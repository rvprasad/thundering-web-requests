#!/usr/bin/python3 server.py

import tornado.ioloop
import tornado.process
import tornado.web
import tornado.log
import json
import logging
import math
import random
from time import process_time_ns


class RandomNumberGenerator(tornado.web.RequestHandler):
    def get(self):
        start = process_time_ns()
        num = int(self.get_argument('num')) if self.get_argument('num') else 10
        randoms = [math.floor(random.random() * 1e6) for _ in range(0, num)]
        self.write(json.dumps(randoms, separators=(',', ':')))
        stop = process_time_ns()
        tornado.log.app_log.info(' {0:0.3f}ms'.format((stop - start) / 1e6))


if __name__ == '__main__':
    tornado.log.app_log.setLevel(logging.INFO)
    app = tornado.web.Application([
        (r'/random', RandomNumberGenerator),
    ])
    app.listen(1234, '0.0.0.0')
    tornado.process.fork_processes(0)
    tornado.ioloop.IOLoop.current().start()
