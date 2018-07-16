import matplotlib.pyplot as plt
import numpy as np

cmap = plt.get_cmap('Set2')
c = np.linspace(0, 1, 10)

plt.style.use('../burin/stylelib/burin.mplstyle')

# set the random seed for the same results every time
np.random.seed(12)

n = 200
axes = []
for i in range(8):
    x = np.random.normal(loc=i, size=n)
    y = np.random.normal(loc=i, size=n)
    ax = plt.scatter(x, y,
                     label='data set %d' % i,
                     color=cmap(c[i]),
                     edgecolor='w')

plt.legend()
plt.title('Default burin scatter plot')
plt.show()

# import matplotlib as mpl
# print(mpl.rcParams)
