#!/usr/bin/env python
#etopo.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#We may need to change this...
npf = np.load("data_sources/ETOPO/etopo_windslow.npz")
X_topo = npf['X']
Y_topo = npf['Y']
Z_topo = npf['Z']
ax.plot_trisurf(X_topo, Y_topo, Z_topo, cmap='winter', linewidth=0.0)

#Choose one file to graph:
npf2 = np.load("data_sources/TEMP_SAL/ctd_HC_binned.npz")
X_bin = npf2['X']
Y_bin = npf2['Y']
Z_bin = npf2['Z']
temp_bin = npf2['temp']
sal_bin = npf2['sal']

#npf3 = np.load("ctd_HC_raw.npz")
#X_raw = npf3['X']
#Y_raw = npf3['Y']
#Z_raw = npf3['Z']
#temp_raw = npf3['temp']
#sal_raw = npf3['sal']

scale = cm.ScalarMappable(cmap='Reds')
color = scale.to_rgba(temp_bin)

#THE DATA FOR STATION 4 IS ACTUALLY TEMP, NEED TO CHANGE
#scale = cm.ScalarMappable(cmap='Reds')
#color = scale.to_rgba(sal_bin)

#for i, _ in enumerate(sal_bin):
#	print sal_bin[i]," ",color[i]

ax.scatter(X_bin, Y_bin, Z_bin, s = 10, c = color, depthshade = False)
plt.show()
