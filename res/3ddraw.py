import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata


def read_file(filename):
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file]

data = [read_file(f"{i}-6servers-32G.txt") for i in range(6)]

fig = plt.figure()


ax = fig.add_subplot(111, projection='3d')


x = np.arange(6)
y = np.arange(len(data[0]))
X, Y = np.meshgrid(x, y)


points = np.array([[i, j] for i in range(6) for j in range(len(data[i]))])
values = np.array([data[i][j] for i in range(6) for j in range(len(data[i]))])


Z = griddata(points, values, (X, Y), method='cubic')


ax.set_zlim(0, 32*1024)

surf = ax.plot_surface(X, Y, Z, cmap='viridis')
surf.set_facecolor('yellow')


ax.set_xlabel('Server')
ax.set_ylabel('Time')
ax.set_zlabel('Memory Usage (MB)')


plt.show()
plt.savefig('1.png')