#! /usr/bin/env python3

import itertools
from collections import namedtuple
import glob
import matplotlib.pyplot as plt
import random
import re
import statistics

# time is in ms
Summary = namedtuple('Summary', ['succ_min_tps', 'succ_med_tps',
                                 'succ_max_tps', 'fail_min_tps',
                                 'fail_med_tps', 'fail_max_tps',
                                 'min_tps', 'med_tps', 'max_tps'])

nodes = ['worker11', 'worker12', 'worker13', 'worker14', 'worker15']
iters = list(range(1, 6))


def get_data(impl, client, nums, reqs, axis):
    succ_req_times = []
    fail_req_times = []
    for i in iters:
        file_names = [glob.glob(f'data/{node}/{impl}/wc-{nums}-{reqs}-{i}-{client}.log')
                      for node in nodes]
        for file_name in [x for x in itertools.chain.from_iterable(file_names)]:
            with open(file_name, 'r') as f:
                for l in f.readlines():
                    mobj1 = re.match(r"^(.*)ms .*ERR(.*)", l)
                    if mobj1:
                        fail_req_times.append(float(mobj1.group(1).strip()))
                        continue

                    mobj2 = re.match(r'^(.*)ms OK$', l)
                    if mobj2:
                        succ_req_times.append(float(mobj2.group(1).strip()))
                        continue

    def helper(x):
        def apply(x, f):
            return f(x) if x else 0

        return (apply(x, min), apply(x, statistics.median), apply(x, max))

    if axis:
        tmp1 = succ_req_times + fail_req_times
        bins = int((max(tmp1) - min(tmp1)) / 10)
        axis.hist(random.sample(tmp1, reqs), bins=bins, alpha=0.5)

    return Summary(*helper(succ_req_times),
                   *helper(fail_req_times),
                   *helper(succ_req_times + fail_req_times))


with open('scripts/reqs-payload-config.txt', 'r') as f:
    tmp1 = (tuple(map(int, x.strip().split(','))) for x in f.readlines())
    reqs_2_nums = {k: [x[1] for x in g] for k, g in itertools.groupby(sorted(tmp1), lambda x: x[0])}

with open(f'data/wc-data.csv', 'wt') as f:
    print("# Service Impl,Client Impl, Num Reqs, Num Nums, "
          "Min Time/Succ Req (ms), Median Time/Succ Req (ms), "
          "Max Time/Succ Req (ms), Min Time/Fail Req (ms), "
          "Median Time/Fail Req (ms), Max Time/Fail Req (ms), "
          "Min Time/Req (ms),  Median Time/Req (ms), Max Time/Req (ms)",
          file=f)
    print(file=f)

    for impl in ['actix-rust', 'go-server']:
        for client in ['go-client', 'httpoison_elixir', 'vertx-kotlin']:
            for reqs in reqs_2_nums:
                if reqs in [100, 2500] and impl == "actix-rust":
                    axis = plt.subplots()[1]
                else:
                    axis = None

                for nums in reqs_2_nums[reqs]:
                    data = get_data(impl, client, nums, reqs, axis)
                    print(f'{impl},{client},{reqs},{nums},'
                          f'{data.succ_min_tps:.3f},{data.succ_med_tps:.3f},'
                          f'{data.succ_max_tps:.3f},{data.fail_min_tps:.3f},'
                          f'{data.fail_med_tps:.3f},{data.fail_max_tps:.3f},'
                          f'{data.min_tps:.3f},{data.med_tps:.3f},'
                          f'{data.max_tps:.3f}', file=f)

                if axis:
                    plt.xlabel("Time per request (ms)")
                    plt.savefig(f'images/wc-actix-rust-{client}-{reqs}.png')
                    plt.clf()

            print(file=f)
            print(file=f)
