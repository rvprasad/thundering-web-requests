#!/usr/bin/python2.7 server.py

import cyclone.web
import json
import math
import random
import sys
from timeit import default_timer as timer

from twisted.internet import reactor
from twisted.python import log


class RandomNumberGenerator(cyclone.web.RequestHandler):
    def get(self):
        start = timer()
        num = int(self.get_argument('num', '10'))
        randoms = ["%06d" % math.floor(random.random() * 999999) for _ in
                   range(0, num)]
        ret = json.dumps(randoms, separators=(',', ':'))
        stop = timer()
        print '{0:0.3f}ms'.format((stop - start) * 1e3)
        self.finish(ret)


def null_log(r):
    pass


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 1234
    application = cyclone.web.Application([
        (r"/random", RandomNumberGenerator)
    ], host, debug=False, log_function=null_log)

    log.startLogging(sys.stdout)
    reactor.listenTCP(port, application)
    print "Serving at %s:%d" % (host, port)
    reactor.run()
