
conc_reqs = [100, 500, 1000, 1500, 3000]

conc_req_and_nums = []
for c in conc_reqs:
    # 2e7, 1e7, and 2e6 are network bandwidth in MBps
    # 5 is the number of worker nodes
    # 9 is the number of bytes occupied by each number on the wire
    conc_req_and_nums.append((c, int(2e7 / (5*9*c))))
    conc_req_and_nums.append((c, int(1e7 / (5*9*c))))
    conc_req_and_nums.append((c, int(2e6 / (5*9*c))))

for i in sorted(conc_req_and_nums, key=lambda x: -x[0]*5*9*x[1]):
    print("{0},{1}".format(i[0], i[1]))
