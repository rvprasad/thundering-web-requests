
conc_reqs = [100, 500, 1000, 1500, 2500]
network_traffic = [2e6, 4e6]

# 5 is the number of worker nodes
# 9 is the number of bytes occupied by each number on the wire
for i in [(c, int(n / (5*9*c))) for c in conc_reqs for n in network_traffic]:
    print("{0},{1}".format(i[0], i[1]))
