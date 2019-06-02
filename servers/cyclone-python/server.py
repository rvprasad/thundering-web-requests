#!/usr/bin/python2.7 server.py

import cyclone.web
import json
import math
import random
import sys

from twisted.internet import reactor
from twisted.python import log


class RandomNumberGenerator(cyclone.web.RequestHandler):
    def get(self):
        num = int(self.get_argument('num', '10'))
        randoms = ["%06d" % math.floor(random.random() * 999999) for _ in
                   range(0, num)]
        self.finish(json.dumps(randoms, separators=(',', ':')))


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 1234
    application = cyclone.web.Application([
        (r"/random", RandomNumberGenerator)
    ], host)

    log.startLogging(sys.stdout)
    reactor.listenTCP(port, application)
    print "Serving at %s:%d" % (host, port)
    reactor.run()
