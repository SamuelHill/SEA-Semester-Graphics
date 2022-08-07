#!/usr/bin/env python
#ctd_HC_converter.py

import csv
import numpy as np

X, Y, Z, temp, sal = [], [], [], [], []

infile = open("ctd_HC_binned.csv", "rU")
reader = csv.reader(infile)
#0 is lat, 1 is long, 2 is depth, 3 is temp, 4 is salinity
for i, row in enumerate(reader):
	if i > 1:
		Y.append(float(row[0]))
		X.append(float(row[1]) - 360.0)
		Z.append(-1 * (float(row[2]) / 111120.0))
		temp.append(float(row[3]))
		sal.append(float(row[4]))
infile.close()

np.savez_compressed("ctd_HC_binned.npz", X=X, Y=Y, Z=Z, temp=temp, sal=sal)

#overwrite previous data (we have already saved it)
X, Y, Z, temp, sal = [], [], [], [], []

infile = open("ctd_HC_raw.csv", "rU")
reader = csv.reader(infile)
#row 0 is station, 1 is lat, 2 is long, 3 is depth, 4 is temp, 5 is salinity
for i, row in enumerate(reader):
	if i > 1:
		Y.append(float(row[1]))
		X.append(float(row[2]) - 360.0)
		Z.append(-1 * (float(row[3]) / 111120.0))
		temp.append(float(row[4]))
		sal.append(float(row[5]))
infile.close()

np.savez_compressed("ctd_HC_raw.npz", X=X, Y=Y, Z=Z, temp=temp, sal=sal)