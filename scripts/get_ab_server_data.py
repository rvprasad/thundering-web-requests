#! /usr/bin/env python3

from collections import namedtuple
import itertools
import re
import statistics


# time in milliseconds
Summary = namedtuple('Summary', ['min_time_per_req', 'mean_time_per_req',
                                 'median_time_per_req', 'max_time_per_req',
                                 'num_serviced_reqs'])


def get_data(impl, nums, reqs):
    impl_2_pattern = {
        'actix-rust': r'^(\d+\.\d+)ms',
        'go-server': r'^(\d+\.\d+)ms',
        'nodejs-express-javascript': r'^\d+: (\d+\.\d+)ms',
        'nodejs-javascript': r'^\d+: (\d+\.\d+)ms',
        'ktor-kotlin': r'^(\d+\.\d+)ms',
        'micronaut-kotlin': r'^(\d+\.\d+)ms',
        'ratpack-kotlin': r'^(\d+\.\d+)ms',
        'vertx-kotlin': r'^(\d+\.\d+)ms',
        'phoenix_elixir': r'^(\d+\.\d+)ms',
        'trot_elixir': r'^(\d+\.\d+)ms',
        'flask+uwsgi-python3': r'^(\d+\.\d+)ms',
        'tornado-python3': r' (\d+\.\d+)ms',
        'cowboy-erlang': r'^(\d+\.\d+)ms'
    }
    result = []
    for i in range(1, 6):
        pattern = impl_2_pattern[impl]
        acc = []
        file_name = f'data/master10/{impl}/ab-{nums}-{reqs}-{i}-server.log'
        try:
            with open(file_name, 'rt') as f:
                tmp1 = (re.search(pattern, l) for l in f)
                tmp2 = (float(mobj.group(1).strip()) for mobj in tmp1 if mobj)
                acc.extend(itertools.islice(tmp2, 200, None))

            result.append(Summary(min(acc), statistics.mean(acc),
                                  statistics.median(acc), max(acc), len(acc)))
        except UnicodeDecodeError as e:
            print(f"Skipping {file_name} due to error {e}")

    return result


with open('scripts/reqs-payload-config.txt', 'r') as f:
    reqs_nums = sorted(tuple(map(int, x.strip().split(',')))
                       for x in f.readlines())

impl_2_min_serviced_reqs = {}
impl_2_max_serviced_reqs = {}
with open(f'data/ab-server-perf.txt', 'wt') as f:
    print("# Num Reqs, Num Nums, Min Time/Req (ms), Mean Time/Req (ms), "
          "Median Time/Req (ms), Max Time/Req (ms), Min Requests/Sec, "
          "Mean Requests/Sec, Median Requests/Sec, Max Requests/Sec, "
          "Num Serviced Requests", file=f)
    for impl in ['actix-rust', 'go-server', 'nodejs-express-javascript',
                 'nodejs-javascript', 'ktor-kotlin', 'micronaut-kotlin',
                 'ratpack-kotlin', 'vertx-kotlin', 'phoenix_elixir',
                 'trot_elixir', 'flask+uwsgi-python3', 'tornado-python3',
                 'cowboy-erlang']:
        print(f'# {impl}', file=f)

        max_serviced_reqs = []
        impl_2_max_serviced_reqs[impl] = max_serviced_reqs
        min_serviced_reqs = []
        impl_2_min_serviced_reqs[impl] = min_serviced_reqs
        for reqs, nums in reqs_nums:
            tmp1 = get_data(impl, nums, reqs)
            tmp1.sort(key=lambda x: -x.num_serviced_reqs)
            if tmp1:
                best_run = tmp1[0]
                print(f'{reqs},{nums},'
                      f'{best_run.min_time_per_req:.3f},'
                      f'{best_run.mean_time_per_req:.3f},'
                      f'{best_run.median_time_per_req:.3f},'
                      f'{best_run.max_time_per_req:.3f},'
                      f'{(1000/best_run.max_time_per_req):.3f},'
                      f'{(1000/best_run.mean_time_per_req):.3f},'
                      f'{(1000/best_run.median_time_per_req):.3f},'
                      f'{(1000/best_run.min_time_per_req):.3f},'
                      f'{best_run.num_serviced_reqs}',
                      file=f)
                max_serviced_reqs.append(best_run.num_serviced_reqs)
                min_serviced_reqs.append(tmp1[-1].num_serviced_reqs)
            else:
                print(f'{reqs},{nums},NA,NA,NA,NA,NA,NA,NA,NA,NA,NA', file=f)
                max_serviced_reqs.append(0)
                min_serviced_reqs.append(0)

        print("", file=f)
        print("", file=f)

with open('data/ab-server-max-serviced-reqs.csv', 'wt') as f:
    print("# X@Y should be interpreted as X requests in Y MBps "
          "configuration", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,2500@2,100@6,500@6,1000@6,"
          "1500@6,2500@6,100@10,500@10,1000@10,1500@10,2500@10", file=f)

    for k, v in impl_2_max_serviced_reqs.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)

with open('data/ab-server-min-serviced-reqs.csv', 'wt') as f:
    print("# X@Y should be interpreted as X requests in Y MBps "
          "configuration", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,2500@2,100@6,500@6,1000@6,"
          "1500@6,2500@6,100@10,500@10,1000@10,1500@10,2500@10", file=f)

    for k, v in impl_2_min_serviced_reqs.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)
