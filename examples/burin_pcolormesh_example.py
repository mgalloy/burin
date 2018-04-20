import matplotlib.pyplot as plt
import numpy as np


# make these smaller to increase the resolution
dx, dy = 0.1, 0.1

# generate 2 2d grids for the x and y bounds
y, x = np.mgrid[-3:3 + dy:dy, -3:3 + dx:dx]
z = (1.0 - x / 2.0 + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)

# x and y are bounds, so z should be the value *inside* those bounds.
# Therefore, remove the last value from the z array.
z = z[:-1, :-1]

# set min/max symmetrically to place 0.0 at the middle of the color map
z_min, z_max = -np.abs(z).max(), np.abs(z).max()

qmesh = plt.pcolormesh(z, vmin=z_min, vmax=z_max, cmap='PRGn')

plt.colorbar()
plt.show()
