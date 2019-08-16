from flask import Flask, request
from timeit import default_timer as timer

import json
import math
import random

app = Flask(__name__)
print("Serving now")


@app.route('/random', methods=['GET'])
def entry():
    start = timer()
    num = int(request.args.get('num', '10'))
    randoms = ["%06d" % math.floor(random.random() * 999999) for _ in
               range(0, num)]
    ret = json.dumps(randoms, separators=(',', ':'))
    stop = timer()
    print('{0:0.3f}ms'.format((stop - start) * 1e3))
    return ret
