#! /usr/bin/env python3

from collections import namedtuple
import glob
import re
import statistics


# time in milliseconds
Summary = namedtuple('Summary', ['min_time_per_req', 'mean_time_per_req',
                                 'median_time_per_req', 'max_time_per_req',
                                 'num_serviced_reqs'])


def get_data(impl, nums, reqs):
    impl_2_pattern = {
        'actix-rust': r'^(\d+\.\d+)ms',
        'go-server': r'(?:1234)?(\d+\.\d+)ms',
        'nodejs-express-javascript': r'^\d+: (\d+\.\d+)ms',
        'nodejs-javascript': r'^\d+: (\d+\.\d+)ms',
        'ktor-kotlin': r'^(\d+\.\d+)ms',
        'micronaut-kotlin': r'^(\d+\.\d+)ms',
        'ratpack-kotlin': r'^(\d+\.\d+)ms',
        'vertx-kotlin': r'^(\d+\.\d+)ms',
        'phoenix_elixir': r'^(\d+\.\d+)ms',
        'trot_elixir': r'^(\d+\.\d+)ms',
        'cyclone-python': r' (\d+\.\d+)ms$',
        'flask+uwsgi-python3': r'^(\d+\.\d+)ms',
        'tornado-python3': r' (\d+\.\d+)ms',
        'yaws-erlang': r' (\d+\.\d+)ms',
        'cowboy-erlang': r'^(\d+\.\d+)ms'
    }
    result = []
    for i in range(1, 3):
        pattern = impl_2_pattern[impl]
        acc = []
        file_name = f'data/master10/{impl}/ab-{nums}-{reqs}-{i}-server.log'
        num_processed_reqs = 0
        with open(file_name, 'rt') as f:
            for l in f.readlines():
                mobj = re.search(pattern, l)
                if mobj:
                    num_processed_reqs += 1
                    if num_processed_reqs > 200:  # disregard warm-up requests
                        acc.append(float(mobj.group(1).strip()))

        result.append(Summary(min(acc), statistics.mean(acc),
                              statistics.median(acc), max(acc), len(acc)))

    result.sort(key=lambda x: -x.num_serviced_reqs)
    return result[0] if result else None


with open('scripts/reqs-payload-config.txt', 'r') as f:
    reqs_nums = sorted(tuple(map(int, x.strip().split(',')))
                       for x in f.readlines())

impl_2_failures = {}
with open(f'data/ab-server-perf.txt', 'wt') as f:
    print("# Num Reqs, Num Nums, Min Time/Req (ms), Mean Time/Req (ms), "
          "Median Time/Req (ms), Max Time/Req (ms), Min Requests/Sec, "
          "Mean Requests/Sec, Median Requests/Sec, Max Requests/Sec, "
          "Num Serviced Requests", file=f)
    for impl in ['actix-rust', 'go-server', 'nodejs-express-javascript',
                 'nodejs-javascript', 'ktor-kotlin', 'micronaut-kotlin',
                 'ratpack-kotlin', 'vertx-kotlin', 'phoenix_elixir',
                 'trot_elixir', 'cyclone-python', 'flask+uwsgi-python3',
                 'tornado-python3', 'yaws-erlang', 'cowboy-erlang']:
        print(f'# {impl}', file=f)

        failures = []
        impl_2_failures[impl] = failures
        for reqs, nums in reqs_nums:
            tmp1 = get_data(impl, nums, reqs)
            if tmp1:
                print(f'{reqs},{nums},'
                      f'{tmp1.min_time_per_req:.3f},'
                      f'{tmp1.mean_time_per_req:.3f},'
                      f'{tmp1.median_time_per_req:.3f},'
                      f'{tmp1.max_time_per_req:.3f},'
                      f'{(1000/tmp1.max_time_per_req):.3f},'
                      f'{(1000/tmp1.mean_time_per_req):.3f},'
                      f'{(1000/tmp1.median_time_per_req):.3f},'
                      f'{(1000/tmp1.min_time_per_req):.3f},'
                      f'{tmp1.num_serviced_reqs}',
                      file=f)
                failures.append(reqs * 5 * 5 - tmp1.num_serviced_reqs)
            else:
                print(f'{reqs},{nums},NA,NA,NA,NA,NA,NA,NA,NA,NA,NA', file=f)
                failures.append(reqs*5)

        print("", file=f)
        print("", file=f)

with open('data/ab-server-data-failures.csv', 'wt') as f:
    print("# X@Y should be interpreted as X requests in Y MBps "
          "configuration", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,3000@2,100@10,500@10,1000@10,"
          "1500@10,3000@10,100@20,500@20,1000@20,1500@20,3000@20", file=f)

    for k, v in impl_2_failures.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)
