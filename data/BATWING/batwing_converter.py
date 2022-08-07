#!/usr/bin/env python
#batwing_converter.py

import csv
import numpy as np

X, Y, Z, temp, sal, fluor = [], [], [], [], [], []

infile = open("winslow_tows.csv", "rU")
reader = csv.reader(infile)
#0 is date, 1 is time, 2 is lat, 3 is long, 4 is depth,
#5 is temp, 6 is salinity, 7 is fluorescence
for i, row in enumerate(reader):
	if i > 1:
		Y.append(float(row[2]))
		X.append(float(row[3]))
		Z.append(-1 * (float(row[4]) / 111120.0))
		temp.append(float(row[5]))
		sal.append(float(row[6]))
		fluor.append(float(row[7]))
infile.close()

np.savez_compressed("batwing.npz", X=X, Y=Y, Z=Z, temp=temp, sal=sal, fluor=fluor)