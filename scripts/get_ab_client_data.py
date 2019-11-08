#! /usr/bin/env python3

import glob
import re
import statistics

nodes = ['worker11', 'worker12', 'worker13', 'worker14', 'worker15']


def get_data(impl, nums, reqs):
    acc1 = []
    for i in range(1, 3):
        acc2 = []
        file_names = [glob.glob(f'data/{node}/{impl}/ab-{nums}-{reqs}-{i}.log')
                      for node in nodes]
        for file_name in [x[0] for x in file_names]:
            time_per_reqs, reqs_per_seq = None, None
            completed_requests, successful_requests = 0, 0
            with open(file_name, 'r') as f:
                for l in f.readlines():
                    mobj1 = re.match(r"Time per request:(.*)\[ms\].*concu.*", l)
                    if mobj1:
                        time_per_reqs = float(mobj1.group(1).strip())
                    mobj2 = re.match(r"Requests per second:(.*)\[#.*", l)
                    if mobj2:
                        reqs_per_seq = float(mobj2.group(1).strip())
                    mobj3 = re.match(r"Total of(.*)requests completed", l)
                    if mobj3:
                        completed_requests = int(mobj3.group(1).strip())
                    mobj4 = re.match(r"Complete requests:(.*)", l)
                    if mobj4:
                        completed_requests = int(mobj4.group(1).strip())
                    mobj5 = re.match(r"Failed requests:(.*)", l)
                    if mobj5:
                        successful_requests = (completed_requests -
                                               int(mobj5.group(1).strip()))
            acc2.append((time_per_reqs, reqs_per_seq, completed_requests,
                         successful_requests))
        acc1.append(acc2)

    return sorted(acc1, key=lambda x: (sum(y[0] is None for y in x),
                                       -sum(y[2] for y in x),
                                       -sum(y[3] for y in x)))


with open('scripts/reqs-payload-config.txt', 'r') as f:
    reqs_nums = sorted(tuple(map(int, x.strip().split(',')))
                       for x in f.readlines())

impl_2_failed_nodes = {}
impl_2_max_compl_succ_reqs = {}
with open(f'data/ab-client-perf.txt', 'wt') as f:
    print("# Num Reqs, Num Nums, Min Time/Req, Mean Time/Req, "
          "Median Time/Req, Max Time/Req, Min Requests/Sec, "
          "Mean Requests/Sec, Median Requests/Sec, Max Requests/Sec, "
          "Num Failed Nodes", file=f)
    for impl in ['actix-rust', 'go-server', 'nodejs-express-javascript',
                 'nodejs-javascript', 'ktor-kotlin', 'micronaut-kotlin',
                 'ratpack-kotlin', 'vertx-kotlin', 'phoenix_elixir',
                 'trot_elixir', 'cyclone-python', 'flask+uwsgi-python3',
                 'tornado-python3', 'yaws-erlang', 'cowboy-erlang']:
        print(f'# {impl}', file=f)

        failed_nodes = []
        impl_2_failed_nodes[impl] = failed_nodes
        max_compl_succ_reqs = []
        impl_2_max_compl_succ_reqs[impl] = max_compl_succ_reqs
        for reqs, nums in reqs_nums:
            data_for_each_run = get_data(impl, nums, reqs)

            compl_and_succ_reqs = [(sum(x[2] for x in y), sum(x[3] for x in y))
                                   for y in data_for_each_run]
            tmp1 = max(compl_and_succ_reqs)
            suffix = '*' if tmp1 != compl_and_succ_reqs[0] else ''
            max_compl_succ_reqs.append(f'{suffix}{tmp1[1]}/{tmp1[0]}')

            least_failing_run = data_for_each_run[0]
            num_failed_nodes = sum(x[0] is None for x in least_failing_run)
            failed_nodes.append(f'{suffix}{num_failed_nodes}')

            if num_failed_nodes == len(nodes):
                print(f'{reqs},{nums},NA,NA,NA,NA,NA,NA,NA,NA,'
                      f'{num_failed_nodes}', file=f)
            else:
                only_succ_clients = [x for x in least_failing_run if x[0]]
                time_per_reqs, reqs_per_sec, _, _ = zip(*only_succ_clients)
                min_time_per_req = min(time_per_reqs)
                mean_time_per_req = statistics.mean(time_per_reqs)
                median_time_per_req = statistics.median(time_per_reqs)
                max_time_per_req = max(time_per_reqs)
                min_reqs_per_sec = min(reqs_per_sec)
                mean_reqs_per_sec = statistics.mean(reqs_per_sec)
                median_reqs_per_sec = statistics.median(reqs_per_sec)
                max_reqs_per_sec = max(reqs_per_sec)
                print(f'{reqs},{nums},{min_time_per_req:.3f},'
                      f'{mean_time_per_req:.3f},{median_time_per_req:.3f},'
                      f'{max_time_per_req:.3f},{min_reqs_per_sec:.3f},'
                      f'{mean_reqs_per_sec:.3f},{median_reqs_per_sec:.3f}',
                      f'{max_reqs_per_sec:.3f},{num_failed_nodes}{suffix}',
                      file=f)

        print("", file=f)
        print("", file=f)

with open('data/ab-client-failed-nodes.csv', 'wt') as f:
    print("# X@Y should be interpreted as X requests in Y MBps "
          "configuration", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,3000@2,100@10,500@10,1000@10,"
          "1500@10,3000@10,100@20,500@20,1000@20,1500@20,3000@20", file=f)

    for k, v in impl_2_failed_nodes.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)

with open('data/ab-client-completed-reqs.csv', 'wt') as f:
    print("# X@Y should be interpreted as X requests in Y MBps "
          "configuration", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,3000@2,100@10,500@10,1000@10,"
          "1500@10,3000@10,100@20,500@20,1000@20,1500@20,3000@20", file=f)

    for k, v in impl_2_max_compl_succ_reqs.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)
