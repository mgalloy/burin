import matplotlib.pyplot as plt
import numpy as np
import scipy.signal


plt.style.use('../burin/stylelib/burin.mplstyle')

# set the random seed for the same results every time
np.random.seed(12)
n = 1000

for i in range(8):
    x = np.arange(n)
    y = np.random.normal(size=n).cumsum()
    y = scipy.signal.savgol_filter(y, 19, 2)

    plt.plot(x, y, label='data set %d' % i)

plt.legend()
plt.show()
