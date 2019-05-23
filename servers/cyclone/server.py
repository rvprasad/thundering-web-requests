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
        num = int(self.get_argument('num')) if self.get_argument('num') else 10
        randoms = map(lambda x: math.floor(random.random() * 1e6),
                      range(0, num))
        self.write(json.dumps(randoms, separators=(',', ':')))


if __name__ == '__main__':
    application = cyclone.web.Application([
        (r"/random", RandomNumberGenerator)
    ], "0.0.0.0")

    log.startLogging(sys.stdout)
    reactor.listenTCP(1234, application)
    reactor.run()
