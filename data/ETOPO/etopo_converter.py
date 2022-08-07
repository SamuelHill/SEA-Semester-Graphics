#!/usr/bin/env python
#etopo_converter.py

#Convert ETOPO to numpy compressed and limit it to windslow reef

#Windslow Reef:
#	Upper left: ldeg S x 175deg 45' W
#	Lower right: 2deg 30' S x 174deg 15' W
#The ETOPO file converts minutes to a base 10 decimal and has
#	the resolution of .5 minutes (offset to .25 and .75). As well,
#	both south and west are considered negative numbers.
#Translated boundaries of Windsor Reef:
#	Upper left: -1.0 x -175.75
#	Lower right: -2.5 x -174.25
#Also, the depths in the ETOPO file are in meters:
#	to scale down to the nautical mile format...
#	depth/1852 = depth in nautical miles
#	to scale to the decimal system given by the lat and long...
#	depth in nautical miles/60 = to scale
#	in other words, divid by 111,120

import csv
import numpy as np

X, Y, Z = [], [], []

infile = open("PIPA_GIS/ETOPO data.csv", "rU")
reader = csv.reader(infile)
#row 0 is the longitude, row 1 is the latitude, row 2 is the depth
for row in reader:
	#because these (lat x long) are negative, reverse the signs from expected:
	long = float(row[0])
#	if long < -174.25 and long > -175.75:
	lat = float(row[1])
#		if lat < -1.0 and lat > -2.5:
	X.append(long)
	Y.append(lat)
	depth = float(row[2])/111120
	Z.append(depth)
infile.close()

np.savez_compressed("etopo_pipa.npz", X=X, Y=Y, Z=Z)

#just a reminder:
#np.savetxt("filename.txt", data #as array#, fmt='%.6f' #what#, delimiter = ' ', newline = '\n', ...)