#!/usr/bin/python

#!/usr/bin/env python
#adcp.py

#TO DO: PROPERLY SCALE U,V,Z TO NAUTICAL MILES

import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

def rescale(a, b, min, max, x):
	top = (b - a) * (x - min)
	bottom = (max - min)
	return (top/bottom) + a

def rescaleDistance(a, b, min, max, x):
	top = (b - a)
	bottom = (max - min)
	print x
	print (top/bottom) * x
	return (top/bottom) * x
	
##prepare graph for plotting...
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

#load adcp data
npf=np.load("adcpS261_all_depths.npz")

#get X,Y,U,V data from the np compressed file:
X_pre = npf['X']
#adjust X coordinates to match ETOPO data...
X_1D = -360 + X_pre
Y_1D = npf['Y']
#X and Y are labeled 1D because after we get the dimensions of U and V
#we want everything to be in the same 2D shape...
U_pre = npf['Ea']
U = U_pre / 111120000.0
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
s = np.where( np.logical_and( np.logical_and(X < -174.25, X > -175.75),
				   np.logical_and(Y < -1.0, Y > -2.5)))
##plot windslow reef adcp data
#ax.quiver(X[s], Y[s], Z[s], U[s], V[s], W[s])

#a = []
#height_scale = 1.5
#all_scale = 10000
#for i in range(0, len(X[s])):
#	z = X[s][i] + 175.75
#	x = Y[s][i] + 2.5
#	y = (Z[s][i] + 0.005) * height_scale
#	b = [x*all_scale, y*all_scale, z*all_scale, U[s][i]*all_scale, V[s][i]*all_scale]
#	#a.append(b)
##print a

newZ = []
mi = min(X[s])
ma = max(X[s])
for i in range(0, len(X[s])):
	# THE MIN AND MAX ARE NEGATIVE SO SWITCH
	re = rescale(-100, 100, ma, mi, X[s][i])
	newZ.append(re)
newU = []
for i in range(0, len(U[s])):
	re = rescaleDistance(-100, 100, ma, mi, U[s][i])
	newU.append(re)
newX = []
mi = min(Y[s])
ma = max(Y[s])
for i in range(0, len(Y[s])):
	# THE MIN AND MAX ARE NEGATIVE SO SWITCH
	re = rescale(-100, 100, ma, mi, Y[s][i])
	newX.append(re)
newV = []
for i in range(0, len(V[s])):
	re = rescaleDistance(-100, 100, ma, mi, V[s][i])
	newV.append(re)
newY = []
mi = min(Z[s])
ma = max(Z[s])
for i in range(0, len(Z[s])):
	re = rescale(0, 10, mi, ma, Z[s][i])
	newY.append(re)

all = []
for i in range(0, len(X[s])):
	current_obs = [newX[i], newY[i], newZ[i], newU[i], newV[i]]
	all.append(current_obs)
print all