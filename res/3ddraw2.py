import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


files = ["0-6servers-32G.txt", "1-6servers-32G.txt", "2-6servers-32G.txt", "3-6servers-32G.txt", "4-6servers-32G.txt", "5-6servers-32G.txt"]


data = []


for i, file in enumerate(files):
    with open(file, 'r') as f:
        lines = f.readlines()
        for j, line in enumerate(lines):
            data.append([i, j, int(line.strip())])


data = np.array(data)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.bar3d(data[:,0], data[:,1], np.zeros(len(data)), 1, 1, data[:,2])


ax.set_xlabel('Server')
ax.set_ylabel('Time')
ax.set_zlabel('Memory Usage (MB)')

plt.show()
plt.savefig('2.png')