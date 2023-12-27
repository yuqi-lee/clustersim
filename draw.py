import numpy as np
import matplotlib.pyplot as plt


coeff = [-1984.129, 4548.033, -3588.554, 1048.644, 252.997]


x = np.arange(0, 1, 0.001)


y = coeff[0]*x**4 + coeff[1]*x**3 + coeff[2]*x**2 + coeff[3]*x + coeff[4]


plt.plot(x, y)
plt.xlabel('Memory Usage')
plt.ylabel('Running Time')
plt.title('Running Time vs Memory Usage')
plt.show()
plt.savefig('./1.png')