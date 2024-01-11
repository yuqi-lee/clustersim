import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


with open('res3.txt', 'r') as f:
    data = [float(line.strip()) for line in f]

with open('res4.txt', 'r') as f:
    data2 = [float(line.strip()) for line in f]

plt.rcParams['font.size'] = 14
print('10000jobs:max = {}, avg = {}, min = {}'.format(max(data2), sum(data2)/len(data2), min(data2)))

data_sorted = np.sort(data)
data2_sorted = np.sort(data2)
p = 1. * np.arange(len(data)) / (len(data) - 1)
p2 = 1. * np.arange(len(data2)) / (len(data2) - 1)

plt.figure(figsize=(8, 5))
l1 = plt.plot(data_sorted, p, color='#00a78e', linewidth=4)
l2 = plt.plot(data2_sorted, p2, color='#f47721', linewidth=4)
l1_patch = mpatches.Patch(color='#00a78e', label='200 jobs on 5 machines')
l2_patch = mpatches.Patch(color='#f47721', label='10000 jobs on 40 machines')

plt.xlim([0.94, 1.23]) 
plt.xlabel('Jobs Throughput Compared to FastSwap')

plt.legend(handles=[l1_patch, l2_patch])

plt.ylabel('CDF')
plt.title('Throughput Improvement CDF')
plt.grid(True)
plt.show()
plt.savefig("throughput.pdf")
plt.savefig("throughput.png")