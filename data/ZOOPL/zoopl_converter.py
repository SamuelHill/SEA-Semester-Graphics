#!/usr/bin/env python
#zoopl_converter.py

import csv
import numpy as np

X, Y, Z, density, diversity = [], [], [], [], []

infile = open("zooplankton_data.csv", "rU")
reader = csv.reader(infile)
#0 Winslow site #, 1 Station ID #, 2 Net type, 3 start lat deg, 4 start lat
#min, 5 start lat ten, 6 start lat hund, 7 start lat dir, 8 start lon deg,
#9 start lon min, 10 start lon ten, 11 start lon hund, 12 start lon dir,
#13 start lat calc., 14 start lon calc., 15 depth of tow (m) *Jan suggested
#this to be the midpoint of the tow, 16 Zoopl density (ml/m3), 17 Shannon-
#Weiner diversity index, 18 Biovolume (ml),
#19 Biomass, 20 Biomass (dry mass of C) (g) ]-> These are empty for now...
for i, row in enumerate(reader):
	if i > 1:
		Y.append(float(row[13]))
		X.append(float(row[14]))
		Z.append(-1 * (float(row[15]) / 111120.0))
		density.append(float(row[16]))
		diversity.append(float(row[17]))
infile.close()

np.savez_compressed("zooplankton.npz", X=X, Y=Y, Z=Z, density=density, diversity=diversity)