#!/usr/bin/env python
#adcp.py

#TO DO: PROPERLY SCALE U,V,Z TO NAUTICAL MILES

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#prepare graph for plotting...
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#load adcp data
npf=np.load("data_sources/ADCP/adcpS261.npz")

#get X,Y,U,V data from the np compressed file:
X_pre = npf['X']
#adjust X coordinates to match ETOPO data...
X_1D = -360 + X_pre
Y_1D = npf['Y']
#X and Y are labeled 1D because after we get the dimensions of U and V
#we want everything to be in the same 2D shape...
U_pre = npf['Ea']
U = U_pre / 111120000.0 #need to properly conver this to scale...
V_pre = npf['No']
V = V_pre / 111120000.0
#the adcp doesn't give a W vector (as it cannot calculate it) so we
#will use an array of all zeros to still pass something but not
#change the directions on each plane
m = U.shape
W = np.zeros(m)
#make X and Y two dimensional
X_tiled = np.tile(X_1D, (m[1], 1))
X = np.transpose(X_tiled)
Y_tiled = np.tile(Y_1D, (m[1], 1))
Y = np.transpose(Y_tiled)
#change depth ranges with d:
#	first bin = 13 -> 23 averaging to 18 meters
#	last bin is dictated by the number of bins given in the adcp file...
last_bin = (m[1] * -10) - 18
d_meters = np.arange(-18, last_bin, -10)
#scale to nautical miles to match etopo data...
d = d_meters / 111120.0
Z = np.tile(d, (m[0], 1))

#find windslow reef in adcp data
s = np.where(np.logical_and( np.logical_and(X < -174.25, X > -175.75),
                   np.logical_and(Y < -1.0, Y  > -2.5)))
#plot windslow reef adcp data
ax.quiver(X[s][::10, ], Y[s][::10, ], Z[s][::10, ], U[s][::10, ], V[s][::10, ], W[s][::10, ], arrow_length_ratio=.01, length=.1) #adjust length/ratio stuff.

#ax.plot(X[s],Y[s],Z[s])

##load etopo data for windslow...
#npf=np.load("data_sources/ETOPO/etopo_windslow.npz")
#X_tri = npf['X']
#Y_tri = npf['Y']
#Z_tri = npf['Z']
##and graph it
#ax.plot_trisurf(X_tri, Y_tri, Z_tri, cmap='winter')

plt.show()