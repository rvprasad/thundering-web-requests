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
    application = cyclone.web.Application([
        (r"/random", RandomNumberGenerator)
    ], "0.0.0.0")

    log.startLogging(sys.stdout)
    reactor.listenTCP(1234, application)
    reactor.run()