#!/usr/bin/env python
#depth_sounder.py

import numpy as np

npf = np.load("data_sources/ETOPO/etopo_windslow.npz")
X = npf['X']
Y = npf['Y']
Z = npf['Z'] * 111120

we_peak = Z[np.where(np.logical_and(np.logical_and(X < -174.60, X > -174.65), np.logical_and(Y < -1.75, Y > -1.80)))]
sw_peak = Z[np.where(np.logical_and(np.logical_and(X < -174.73, X > -174.75), np.logical_and(Y < -1.89, Y > -1.91)))]
channel = Z[np.where(np.logical_and(np.logical_and(X < -174.74, X > -174.78), np.logical_and(Y < -1.77, Y > -1.82)))]

#this one may need to be altered:
reeftop = Z[np.where(np.logical_and(np.logical_and(X < -174.91, X > -174.99), np.logical_and(Y < -1.75, Y > -1.80)))]

deepchn = Z[np.where(np.logical_and(np.logical_and(X < -175.09, X > -175.10), np.logical_and(Y < -1.64, Y > -1.68)))]
ea_peak = Z[np.where(np.logical_and(np.logical_and(X < -175.19, X > -175.21), np.logical_and(Y < -1.70, Y > -1.72)))]

print "western peak:    ",min(we_peak)," ",max(we_peak)
print "south-west peak: ",min(sw_peak)," ",max(sw_peak)
print "western channel: ",min(channel)," ",max(channel)
print "main reef peak:  ",min(reeftop)," ",max(reeftop)
print "eastern channel: ",min(deepchn)," ",max(deepchn)
print "eastern peak:    ",min(ea_peak)," ",max(ea_peak)