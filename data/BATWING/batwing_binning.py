#!/usr/bin/env python
#batwing_binning.py

import numpy as np
import math
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

npf = np.load("batwing.npz")
X = npf['X']
Y = npf['Y']
Z = npf['Z']
temp = npf['temp']
sal = npf['sal']
fluor = npf['fluor']


fig = plt.figure()
ax = fig.add_subplot(111)
#ax.scatter(X, Y, Z, cmap='winter')
ax.plot(range(0,len(X)),(Z * 111120))
plt.show()

#X_bin, Y_bin, Z_bin, temp_bin, sal_bin, fluor_bin = [], [], [], [], [], []

#num_bins = (((min(Z) * 111120) + 3) / -10) + 1
#max_bin_depth = (num_bins * -10) - 13
##bins = np.insert(np.arange(-13, max_bin_depth - 1, -10.0), 0, 0)
#bins = np.arange(-13, max_bin_depth - 1, -10.0)

#up_and_down = [0]
#bins = []
#for i, depth in enumerate(Z):
#	if i != 0 and i != (len(Z) - 1):
#		if Z[i - 1] > depth and Z[i + 1] > depth:
#			up_and_down.append(i)
#		elif Z[i - 1] < depth and Z[i + 1] < depth:
#			up_and_down.append(i)

#for i, _ in enumerate(up_and_down):
#	if i != (len(up_and_down) - 1):
#		Xs = X[up_and_down[i]:up_and_down[i + 1]]
#		Ys = Y[up_and_down[i]:up_and_down[i + 1]]
#		Zs = Z[up_and_down[i]:up_and_down[i + 1]]
#		temps = temp[up_and_down[i]:up_and_down[i + 1]]
#		sals = sal[up_and_down[i]:up_and_down[i + 1]]
#		fluors = fluor[up_and_down[i]:up_and_down[i + 1]]
#		bins.append([Xs, Ys, Zs, temps, sals, fluors])
#	else:
#		Xs = X[up_and_down[i] + 1:]
#		Ys = Y[up_and_down[i] + 1:]
#		Zs = Z[up_and_down[i] + 1:]
#		temps = temp[up_and_down[i] + 1:]
#		sals = sal[up_and_down[i] + 1:]
#		fluors = fluor[up_and_down[i] + 1:]
#		bins.append([Xs, Ys, Zs, temps, sals, fluors])

#print bins[0][2] * 111120
#print bins[1][2] * 111120