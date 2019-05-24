from flask import Flask, request
from time import process_time_ns

import json
import math
import random

app = Flask(__name__)


@app.route('/random', methods=['GET'])
def entry():
    start = process_time_ns()
    num = int(request.args.get('num', '10'))
    randoms = [math.floor(random.random() * 1e6) for _ in range(0, num)]
    ret = json.dumps(randoms, separators=(',', ':'))
    stop = process_time_ns()
    print('{0:0.3f}ms'.format((stop - start) / 1e6))
    return ret
