#! /usr/bin/env python3

from collections import namedtuple
import glob
import re
import statistics

Summary = namedtuple('Summary', ['time_per_reqs', 'reqs_per_sec',
                                 'completed_requests', 'successful_requests'])

nodes = ['worker11', 'worker12', 'worker13', 'worker14', 'worker15']
iters = list(range(1, 6))


def get_data(impl, nums, reqs):
    acc1 = []
    for i in iters:
        acc2 = []
        file_names = [glob.glob(f'data/{node}/{impl}/ab-{nums}-{reqs}-{i}.log')
                      for node in nodes]
        for file_name in [x[0] for x in file_names]:
            time_per_reqs, reqs_per_sec = None, None
            completed_requests, successful_requests = 0, 0
            with open(file_name, 'r') as f:
                for l in f.readlines():
                    mobj1 = re.match(r"Time per request:(.*)\[ms\].*concu.*", l)
                    if mobj1:
                        time_per_reqs = float(mobj1.group(1).strip())
                        continue

                    mobj2 = re.match(r"Requests per second:(.*)\[#.*", l)
                    if mobj2:
                        reqs_per_sec = float(mobj2.group(1).strip())
                        continue

                    mobj3 = re.match(r"Total of(.*)requests completed", l)
                    if mobj3:
                        completed_requests = int(mobj3.group(1).strip())
                        continue

                    mobj4 = re.match(r"Complete requests:(.*)", l)
                    if mobj4:
                        completed_requests = int(mobj4.group(1).strip())
                        continue

                    mobj5 = re.match(r"Failed requests:(.*)", l)
                    if mobj5:
                        successful_requests = (completed_requests -
                                               int(mobj5.group(1).strip()))

            acc2.append(Summary(time_per_reqs, reqs_per_sec, completed_requests,
                                successful_requests))
        acc1.append(acc2)

    return acc1


def key_helper(acc):
    key1 = sum(x.time_per_reqs is None for x in acc)
    key2 = -sum(x.completed_requests for x in acc)
    key3 = -sum(x.successful_requests for x in acc)
    tmp1 = [x for x in acc if x.time_per_reqs]
    key4 = -statistics.median(x.reqs_per_sec for x in tmp1) if tmp1 else 0
    return key1, key2, key3, key4


def get_stats(items):
    return min(items), statistics.mean(items), statistics.median(items), max(items)


with open('scripts/reqs-payload-config.txt', 'r') as f:
    reqs_nums = sorted(tuple(map(int, x.strip().split(',')))
                       for x in f.readlines())

impl_2_failed_nodes = {}
impl_2_max_compl_succ_reqs = {}
impl_2_min_compl_succ_reqs = {}
with open(f'data/ab-client-perf.txt', 'wt') as f:
    print("# Num Reqs, Num Nums, Min Time/Req (ms), Mean Time/Req (ms), "
          "Median Time/Req (ms), Max Time/Req (ms), Min Requests/Sec, "
          "Mean Requests/Sec, Median Requests/Sec, Max Requests/Sec, "
          "Num Failed Nodes", file=f)
    for impl in ['actix-rust', 'go-server', 'nodejs-express-javascript',
                 'nodejs-javascript', 'ktor-kotlin', 'micronaut-kotlin',
                 'ratpack-kotlin', 'vertx-kotlin', 'phoenix_elixir',
                 'trot_elixir', 'flask+uwsgi-python3', 'tornado-python3',
                 'cowboy-erlang']:
        print(f'# {impl}', file=f)

        failed_nodes = []
        impl_2_failed_nodes[impl] = failed_nodes
        max_compl_succ_reqs = []
        impl_2_max_compl_succ_reqs[impl] = max_compl_succ_reqs
        min_compl_succ_reqs = []
        impl_2_min_compl_succ_reqs[impl] = min_compl_succ_reqs
        for reqs, nums in reqs_nums:
            tmp1 = get_data(impl, nums, reqs)
            data_for_each_run = sorted(tmp1, key=key_helper)

            compl_and_succ_reqs = [(sum(x.completed_requests for x in y),
                                    sum(x.successful_requests for x in y))
                                   for y in data_for_each_run]
            tmp2 = max(compl_and_succ_reqs)
            suffix = '*' if tmp2 != compl_and_succ_reqs[0] else ''
            max_compl_succ_reqs.append(f'{suffix}{tmp2[1]}/{tmp2[0]}')
            tmp3 = min(compl_and_succ_reqs)
            min_compl_succ_reqs.append(f'{suffix}{tmp3[1]}/{tmp3[0]}')

            least_num_failed_nodes = sum(x.time_per_reqs is None
                                         for x in data_for_each_run[0])
            most_num_failed_nodes = sum(x.time_per_reqs is None
                                        for x in data_for_each_run[-1])
            failed_nodes.append(f'{suffix}{least_num_failed_nodes}/{most_num_failed_nodes}')

            if least_num_failed_nodes == len(nodes):
                print(f'{reqs},{nums},NA,NA,NA,NA,NA,NA,NA,NA,'
                      f'{least_num_failed_nodes}/{most_num_failed_nodes}',
                      file=f)
            else:
                run_to_consider = data_for_each_run[0]
                only_succ_clients = filter(lambda x: x.time_per_reqs,
                                           run_to_consider)
                time_per_reqs, reqs_per_sec, _, _ = zip(*only_succ_clients)
                tpr_stats = get_stats(time_per_reqs)
                rps_stats = get_stats(reqs_per_sec)
                print(f'{reqs},{nums},{tpr_stats[0]:.3f},'
                      f'{tpr_stats[1]:.3f},{tpr_stats[2]:.3f},'
                      f'{tpr_stats[3]:.3f},{rps_stats[0]:.3f},'
                      f'{rps_stats[1]:.3f},{rps_stats[2]:.3f},'
                      f'{rps_stats[3]:.3f},'
                      f'{least_num_failed_nodes}/{most_num_failed_nodes}{suffix}',
                      file=f)

        print("", file=f)
        print("", file=f)

with open('data/ab-client-failed-nodes.csv', 'wt') as f:
    print("# X@Y should be interpreted as X requests in Y MBps "
          "configuration", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,2500@2,100@6,500@6,1000@6,"
          "1500@6,2500@6,100@10,500@10,1000@10,1500@10,2500@10", file=f)

    for k, v in impl_2_failed_nodes.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)

with open('data/ab-client-completed-reqs.csv', 'wt') as f:
    print("# X@Y should be interpreted as X requests in Y MBps "
          "configuration", file=f)
    print("# A/B should be interpreted as A successful requests "
          "amongst B completed requests", file=f)

    print("Max completed reqs", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,2500@2,100@6,500@6,1000@6,"
          "1500@6,2500@6,100@10,500@10,1000@10,1500@10,2500@10", file=f)
    for k, v in impl_2_max_compl_succ_reqs.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)

    print(file=f)
    print("Min completed reqs", file=f)
    print("Impl,100@2,500@2,1000@2,1500@2,2500@2,100@6,500@6,1000@6,"
          "1500@6,2500@6,100@10,500@10,1000@10,1500@10,2500@10", file=f)
    for k, v in impl_2_min_compl_succ_reqs.items():
        print("{0},{1},{4},{7},{10},{13},{2},{5},{8},{11},{14}"
              ",{3},{6},{9},{12},{15}".format(k, *v), file=f)
