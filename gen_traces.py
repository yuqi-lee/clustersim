import workloads_simu as workloads
import subprocess

import random
import math
import os


#workload1 = ['pagerank', 'xsbench']
#workload2 = [ 'xgboost', 'snappy', 'redis']
selected_workloads = ['xgboost', 'snappy', 'redis']
f1 = open('throughoup_3workloads/random_trace.sh', 'w')
f2 = open('throughoup_3workloads/random_trace_fastswap.sh', 'w')
f3 = open('throughoup_3workloads/res.txt', 'w')

max_far = 163840


for i in range(500):
    #selected_workload1 = random.sample(workload1, random.choice([0, 1, 2]))
    #elected_workload2 = random.sample(workload2, random.choice([3]))


    #selected_workloads = selected_workload1 + selected_workload2
    #selected_workloads = workload1 + selected_workload2

    min_time = min(workloads.get_workload_class(w).y[0] for w in selected_workloads)
    min_mem = min(workloads.get_workload_class(w).ideal_mem for w in selected_workloads)
    #workload_values = [(min_time / workloads.get_workload_class(w).y[0]) * (min_mem / workloads.get_workload_class(w).ideal_mem) * (0.3 + 1 - workloads.get_workload_class(w).min_ratio) for w in selected_workloads]
    #workload_values = [random.uniform(0.9, 1.1) * (workloads.get_workload_class(w).ideal_mem / min_mem) * (0.05 + (1 - workloads.get_workload_class(w).min_ratio) if workloads.get_workload_class(w).min_ratio < 1 else 0.39) for w in selected_workloads]
    #print(workload_values)
    
    workload_values = [random.uniform(1, 4.5) for w in selected_workloads]
    total_value = sum(workload_values)
    workload_ratios = [round(100 * v / total_value) for v in workload_values]


    while sum(workload_ratios) > 100:
        max_index = workload_ratios.index(max(workload_ratios))
        workload_ratios[max_index] -= 1
    while sum(workload_ratios) < 100:
        min_index = workload_ratios.index(min(workload_ratios))
        workload_ratios[min_index] += 1

  
    #delta = random.randint(10, 10)
    #if workload_ratios[1] + 2*delta > 5 and workload_ratios[1] + 2*delta < 85 and \
        #workload_ratios[0] - delta > 5 and  workload_ratios[0] - delta < 85 and \
        #workload_ratios[2] - delta > 5 and  workload_ratios[2] - delta < 85:
        #workload_ratios[1] += 2*delta
        #workload_ratios[0] -= delta + 1
        #workload_ratios[2] -= delta - 1  

    workload_min_ratios = [int(workloads.get_workload_class(w).min_ratio * 100) for w in selected_workloads]
    
    rand = random.randint(1,10000)
    trace = 'python simulation_one_time.py' + ' ' + '{}'.format(rand) + ' ' + '--num_servers 5 --cpus 32 --mem 81920' + ' '\
            + '--workload ' + ','.join(selected_workloads) + '   ' + '--use_shrink' + ' '\
            + '--ratios ' + ':'.join(map(str, workload_ratios)) + ' ' \
            + '--workload_ratios ' + ','.join(map(str, workload_min_ratios)) + ' '\
            + '--remotemem --until 200 --size 200 --max_far {}'.format(max_far)

    trace2 = 'python simulation_one_time.py' + ' ' + '{}'.format(rand) + ' ' + '--num_servers 5 --cpus 32 --mem 81920' + ' '\
            + '--workload ' + ','.join(selected_workloads) + '   ' + '--use_shrink' + ' '\
            + '--ratios ' + ':'.join(map(str, workload_ratios)) + ' ' \
            + '--workload_ratios ' + ','.join(map(str, workload_min_ratios)) + ' '\
            + '--remotemem --until 200 --size 200 --max_far {}'.format(max_far) + ' ' + '--use_fastswap'
    
    process1 = subprocess.Popen(trace, shell=True, stdout=subprocess.PIPE)
    output1, error = process1.communicate()

    process2 = subprocess.Popen(trace2, shell=True, stdout=subprocess.PIPE)
    output2, error = process2.communicate()

    output1 = output1.decode("utf-8").strip()
    output2 = output2.decode("utf-8").strip()

    f1.write(str(trace) + '\n')
    f2.write(str(trace2) + '\n')
    f3.write('{}'.format(float(output2)/float(output1)) + ' \n')  

    f1.flush()
    f2.flush()
    f3.flush() 