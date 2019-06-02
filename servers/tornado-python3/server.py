#!/usr/bin/python3 server.py

import tornado.ioloop
import tornado.process
import tornado.web
import tornado.log
import json
import logging
import math
import random
from timeit import default_timer as timer


class RandomNumberGenerator(tornado.web.RequestHandler):
    def get(self):
        start = timer()
        num = int(self.get_argument('num', '10'))
        randoms = ["%06d" % math.floor(random.random() * 999999) for _ in
                   range(0, num)]
        ret = json.dumps(randoms, separators=(',', ':'))
        stop = timer()
        tornado.log.app_log.info(' {0:0.3f}ms'.format((stop - start) * 1e3))
        self.finish(ret)


if __name__ == '__main__':
    tornado.log.app_log.setLevel(logging.INFO)
    app = tornado.web.Application([
        (r'/random', RandomNumberGenerator),
    ])
    app.listen(1234, '0.0.0.0')
    tornado.process.fork_processes(0)
    tornado.ioloop.IOLoop.current().start()
