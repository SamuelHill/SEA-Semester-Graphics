#!/usr/bin/python

import numpy as np

def rescale(a, b, min, max, x):
	top = (b - a) * (x - min)
	bottom = (max - min)
	return (top/bottom) + a

npf = np.load("etopo_windslow.npz")

X = npf['X']
Y = npf['Y']
Z = npf['Z']

newZ = []
mi = min(X)
ma = max(X)
for i in range(0, len(X)):
	# THE MIN AND MAX ARE NEGATIVE SO SWITCH
	re = rescale(-1000, 1000, ma, mi, X[i])
	newZ.append(re)
newX = []
mi = min(Y)
ma = max(Y)
for i in range(0, len(Y)):
	# THE MIN AND MAX ARE NEGATIVE SO SWITCH
	re = rescale(-1000, 1000, ma, mi, Y[i])
	newX.append(re)
newY = []
mi = min(Z)
ma = max(Z)
for i in range(0, len(Z)):
	re = rescale(0, -100, ma, mi, Z[i])
	newY.append(re)

all = []
for i in range(0, len(X)):
	current_obs = [newX[i], newY[i], newZ[i]]
	all.append(current_obs)

print len(all)

print "var topo = ["
for i in range(0, len(X) - 1):
	#if "e" not in str(all[i]):
	print "\t" + str(all[i]) + ","
print "\t" + str(all[i + 1])
print "]"