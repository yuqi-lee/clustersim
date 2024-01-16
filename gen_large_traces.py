import itertools
import random
import workloads_simu as workloads
import subprocess

max_far = 1310720

workload1 = ['pagerank', 'xsbench']
workload2 = [ 'xgboost', 'redis','snappy']


def find_combinations():
    # Generate all combinations of 5 numbers that sum to 100
    combinations = [seq for seq in itertools.combinations(range(10, ), 5) if sum(seq) == 100]
    
    # Remove duplicates (same combinations in different orders)
    combinations = [tuple(sorted(seq)) for seq in combinations]
    combinations = sorted(combinations, key=lambda x: (x[0], x[1], x[2], x[3], x[4]))
    combinations = list(k for k,_ in itertools.groupby(combinations))
    
    return combinations

combinations = find_combinations()
#f1 = open('mr_res/random_large_trace.sh', 'w')
f1 = open('mr_res/res3_large.txt', 'w')
f2 = open('mr_res/trace.txt', 'w')

selected_workloads = workload1 + workload2
workload_min_ratios = [int(workloads.get_workload_class(w).min_ratio * 100) for w in selected_workloads]

for combo in combinations:
    cmd = 'python simulation_one_time.py' + ' ' + '{}'.format(random.randint(1,10000)) + ' ' + '--num_servers 40 --cpus 32 --mem 81920' + ' '\
            + '--workload ' + ','.join(selected_workloads) + '   ' + '--use_shrink' + ' '\
            + '--ratios ' + '{}:{}:{}:{}:{}'.format(combo[0],combo[1],combo[2],combo[3],combo[4]) + ' ' \
            + '--workload_ratios ' + ','.join(map(str, workload_min_ratios)) + ' '\
            + '--remotemem --until 2000 --size 10000 --max_far {}'.format(max_far)
    
    process1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output1, error = process1.communicate()

    cmd += ' --use_fastswap' + ' '
    process2 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output2, error = process2.communicate()

    output1 = output1.decode("utf-8").strip()
    output2 = output2.decode("utf-8").strip()
    #print(output1)
    #print(output2)
    f1.write('{}'.format(float(output2)/float(output1)) + ' \n')   
    f2.write('{}:{}:{}:{}:{} \t  MrAllocSwap:{}, FastSwap:{} \n'.format(combo[0],combo[1],combo[2],combo[3],combo[4], int(output1), int(output2)))
    f1.flush()
    f2.flush()
    
    


