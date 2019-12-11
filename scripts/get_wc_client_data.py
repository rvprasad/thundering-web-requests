#! /usr/bin/env python3

from collections import defaultdict, namedtuple
import glob
import re
import statistics

# time is in ms
Summary = namedtuple('Summary', ['median_time_per_req',
                                 'median_time_per_succ_req',
                                 'median_time_per_fail_req',
                                 'num_succ_reqs', 'num_fail_reqs',
                                 'num_failed_nodes', 'reqs_per_sec',
                                 'failure_2_freq'])

nodes = ['worker11', 'worker12', 'worker13', 'worker14', 'worker15']
iters = list(range(1, 6))


def get_median(col):
    return statistics.median(col) if col else None


def get_data(impl, nums, reqs):
    acc = []
    for i in iters:
        successful_req_times = []
        failed_req_times = []
        num_failed_nodes = 0
        total_time = 0
        failure_2_freq = defaultdict(int)
        file_names = [glob.glob(f'data/{node}/{impl}/wc-{nums}-{reqs}-{i}-*.log')
                      for node in nodes]
        for file_name in [x[0] for x in file_names]:
            succ_req_times, fail_req_times = [], []
            with open(file_name, 'r') as f:
                for l in f.readlines():
                    mobj1 = re.match(r"^(.*)ms .*ERR(.*)", l)
                    if mobj1:
                        fail_req_times.append(float(mobj1.group(1).strip()))
                        if mobj1.lastindex == 2:
                            failure_2_freq[mobj1.group(2).strip()] += 1
                        continue

                    mobj2 = re.match(r'^(.*)ms OK$', l)
                    if mobj2:
                        succ_req_times.append(float(mobj2.group(1).strip()))
                        continue

                    mobj3 = re.match(r"^Success: (\d+)$", l)
                    if mobj3:
                        assert int(mobj3.group(1).strip()) == len(succ_req_times)
                        continue

                    mobj4 = re.match(r"^Failure: (\d+)$", l)
                    if mobj4:
                        assert int(mobj4.group(1).strip()) == len(fail_req_times)
                        continue

                    mobj5 = re.match(r"^real\s+(\d+)m(.*)s$", l)
                    if mobj5:
                        secs = float(mobj5.group(2).strip())
                        secs += int(mobj5.group(1).strip()) * 60
                        total_time += secs
                        continue

            if succ_req_times == 0:
                num_failed_nodes += 1

            successful_req_times.extend(succ_req_times)
            failed_req_times.extend(fail_req_times)

        acc.append(Summary(
                get_median(successful_req_times + failed_req_times),
                get_median(successful_req_times),
                get_median(failed_req_times),
                len(successful_req_times), len(failed_req_times),
                num_failed_nodes,
                (len(successful_req_times) + len(failed_req_times)) / total_time,
                failure_2_freq))

    return acc


def key_helper1(summary):
    key1 = -summary.num_succ_reqs - summary.num_fail_reqs
    key2 = -summary.num_succ_reqs
    return key1, key2


def key_helper2(summary):
    key1 = summary.reqs_per_sec
    key2 = key_helper1(summary)
    return key1, key2


def get_compl_succ_reqs(summary, reqs):
    ret = ''
    if summary.num_fail_reqs:
        prefix = '' if summary.num_fail_reqs < len(nodes) * reqs * .05 else '*'
        ret = (f'{prefix}{summary.failure_2_freq["checkout_timeout"]}/'
               f'{summary.failure_2_freq["connect_timeout"]}/'
               f'{summary.failure_2_freq["timeout"]}/'
               f'{summary.failure_2_freq["closed"]}/'
               f'{summary.failure_2_freq[""]}')

    return ret


with open('scripts/reqs-payload-config.txt', 'r') as f:
    reqs_nums = sorted(tuple(map(int, x.strip().split(',')))
                       for x in f.readlines())

impl_2_failed_nodes = {}
impl_2_max_failed_reqs = {}
impl_2_min_failed_reqs = {}
with open(f'data/wc-client-perf.txt', 'wt') as f:
    print("# Num Reqs, Num Nums, Median Time/Succ Req (ms), "
          "Median Time/Fail Req (ms), Reqs/Sec, Num Succ Reqs, Num Fail Reqs,",
          file=f)
    for impl in ['actix-rust', 'go-server', 'nodejs-express-javascript',
                 'nodejs-javascript', 'ktor-kotlin', 'micronaut-kotlin',
                 'ratpack-kotlin', 'vertx-kotlin', 'phoenix_elixir',
                 'trot_elixir', 'flask+uwsgi-python3', 'tornado-python3',
                 'cowboy-erlang']:
        print(f'# {impl}', file=f)

        failed_nodes = []
        impl_2_failed_nodes[impl] = failed_nodes
        max_failed_reqs = []
        impl_2_max_failed_reqs[impl] = max_failed_reqs
        min_failed_reqs = []
        impl_2_min_failed_reqs[impl] = min_failed_reqs
        for reqs, nums in reqs_nums:
            tmp1 = get_data(impl, nums, reqs)
            least_num_failed_nodes = min(x.num_failed_nodes for x in tmp1)
            most_num_failed_nodes = max(x.num_failed_nodes for x in tmp1)
            failed_nodes.append(
                    f'{least_num_failed_nodes}/{most_num_failed_nodes}')
            tmp2 = sorted(tmp1, key=key_helper1)
            max_failed_reqs.append(get_compl_succ_reqs(tmp2[0], reqs))
            min_failed_reqs.append(get_compl_succ_reqs(tmp2[-1], reqs))

            if least_num_failed_nodes == len(nodes):
                print(f'{reqs},{nums},NA,NA,NA,NA,NA,'
                      f'{least_num_failed_nodes}/{most_num_failed_nodes}',
                      file=f)
            else:
                run = sorted(tmp1, key=key_helper2)[0]
                if run.num_fail_reqs:
                    tmp3 = f'{run.median_time_per_fail_req:.3f}'
                else:
                    tmp3 = 0

                print(f'{reqs},{nums},{run.median_time_per_req:.3f},'
                      f'{run.median_time_per_succ_req:.3f},{tmp3},'
                      f'{run.reqs_per_sec:.3f},'
                      f'{run.num_succ_reqs},{run.num_fail_reqs},'
                      f'{least_num_failed_nodes}/{most_num_failed_nodes}',
                      file=f)

        print("", file=f)
        print("", file=f)

with open('data/wc-client-failed-nodes.csv', 'wt') as f:
    print("# X@Y denotes X requests in Y MBps configuration", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,2500@2,100@6,500@6,1000@6,"
          "1500@6,2500@6,100@10,500@10,1000@10,1500@10,2500@10", file=f)

    for k, v in impl_2_failed_nodes.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)

with open('data/wc-client-failed-reqs.csv', 'wt') as f:
    print("# X@Y denotes X requests in Y MBps configuration", file=f)
    print("# A/B/C/D/U should be read as requests failed with A "
          "checkout_timeout errors, B connect_timeout errors, C timeout "
          "errors, D closed errors, and E unknown errors.", file=f)

    print("Max failed reqs", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,2500@2,100@6,500@6,1000@6,"
          "1500@6,2500@6,100@10,500@10,1000@10,1500@10,2500@10", file=f)
    for k, v in impl_2_max_failed_reqs.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)

    print(file=f)
    print("Min failed reqs", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,2500@2,100@6,500@6,1000@6,"
          "1500@6,2500@6,100@10,500@10,1000@10,1500@10,2500@10", file=f)
    for k, v in impl_2_min_failed_reqs.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)
