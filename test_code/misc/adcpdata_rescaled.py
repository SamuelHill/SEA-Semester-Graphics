#!/usr/bin/python

import numpy as np
import math

def rescale(a, b, min, max, x):
	top = (b - a) * (x - min)
	bottom = (max - min)
	return (top/bottom) + a

def rescaleDistance(a, b, min, max, x):
	top = (b - a)
	bottom = (max - min)
	return (top/bottom) * x

npf=np.load("adcpS261_all_depths.npz")

U_pre = npf['Ea']
U = U_pre / 111120000.0
m = U.shape

V_pre = npf['No']
V = V_pre / 111120000.0

# UNUSED
W = np.zeros(m)

X_pre = npf['X']
X_1D = -360 + X_pre
X_tiled = np.tile(X_1D, (m[1], 1))
X = np.transpose(X_tiled)

Y_1D = npf['Y']
Y_tiled = np.tile(Y_1D, (m[1], 1))
Y = np.transpose(Y_tiled)

last_bin = (m[1] * -10) - 18
d_meters = np.arange(-18, last_bin, -10)
d = d_meters / 111120.0
Z = np.tile(d, (m[0], 1))

#find windslow reef in adcp data
s = np.where(np.logical_and(np.logical_and(X<-174.25, X>-175.75), np.logical_and(Y<-1.0, Y>-2.5)))

newZ = []
mi = min(X[s])
ma = max(X[s])
for i in range(0, len(X[s])):
	# THE MIN AND MAX ARE NEGATIVE SO SWITCH
	re = rescale(-1000, 1000, ma, mi, X[s][i])
	newZ.append(re)
newU = []
for i in range(0, len(U[s])):
	if (U[s][i] < -0.1 or U[s][i] > 0.1):
		u = 0
	else:
		u = U[s][i]
	re = rescaleDistance(-1000, 1000, ma, mi, u)
	newU.append(re)

#print newU

newX = []
mi = min(Y[s])
ma = max(Y[s])
for i in range(0, len(Y[s])):
	# THE MIN AND MAX ARE NEGATIVE SO SWITCH
	re = rescale(-1000, 1000, ma, mi, Y[s][i])
	newX.append(re)
newV = []
for i in range(0, len(V[s])):
	if (V[s][i] < -0.1 or V[s][i] > 0.1):
		v = 0
	else:
		v = V[s][i]
	re = rescaleDistance(-1000, 1000, ma, mi, v)
	newV.append(re)
# V[s][i] <--- last element is too big.

npf = np.load("etopo_windslow.npz")
Z_topo = npf['Z']
newY = []
mi = min(Z_topo)
ma = max(Z_topo)
for i in range(0, len(Z[s])):
	re = rescale(0, -100, ma, mi, Z[s][i])
	newY.append(re)

all = []
for i in range(0, len(X[s])):
	mag = math.sqrt(math.pow(U_pre[s][i],2) + math.pow(V_pre[s][i],2))
	current_obs = [newX[i], newY[i], newZ[i], newU[i], newV[i], X[s][i], Y[s][i], Z[s][i]*111120.0, mag]
	all.append(current_obs)

print "var currents = ["
for i in range(0, len(X[s]) - 1):
	#if "e" not in str(all[i]):
	print "\t" + str(all[i]) + ","
print "\t" + str(all[i + 1])
print "]"