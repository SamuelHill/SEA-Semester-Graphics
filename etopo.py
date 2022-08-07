#!/usr/bin/env python
#etopo.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

npf = np.load("data_sources/ETOPO/etopo_windslow.npz")
X = npf['X']
Y = npf['Y']
Z = npf['Z']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(X[::3,], Y[::3,], Z[::3,], cmap='winter', linewidth=0.0)
plt.show()