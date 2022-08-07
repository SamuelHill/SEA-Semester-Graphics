'''
 ADCP variables
        dimensions: N_STATIONS, N_SAMPLES = 60 ;
        float longitude(N_STATIONS) ;
        float latitude(N_STATIONS) ;
        double date_time(N_STATIONS) ;
        float var1(N_STATIONS, N_SAMPLES) ; "Depth" 
        float var2(N_STATIONS, N_SAMPLES) ; "Echo Amplitude"
        float var3(N_STATIONS, N_SAMPLES) ; "East Component" ;"mm/s"
        float var4(N_STATIONS, N_SAMPLES) ; "North Component" ;"mm/s"
        float var5(N_STATIONS, N_SAMPLES) ; "Magnitude" ;"mm/s"
        float var6(N_STATIONS, N_SAMPLES) ; "Direction" ;"deg"
        float var7(N_STATIONS, N_SAMPLES) ; "Ensemble"
'''
# This program draw histogram of echo for one bin (check abin to change the ADCP bin)
#  type python RdADCP.py Sxxx
#
#  To plot vector with gmt(psxy) prepare file X,Y,dir,len (XYDL)
#  This is meant for the Pipa area (can be adapted for any area)
#
#  To plot vector with matplot prepare file X,Y,U,V
#

import sys
import numpy as np
import numpy.ma as ma
#from netCDF4 import Dataset
import math
## Extract data from file *********************************
#ncfile = Dataset('../NADCP/S254_ADCP.nc','r') 
#lat = ncfile.variables['latitude'][:]
#lon = ncfile.variables['longitude'][:]
#time = ncfile.variables['date_time'][:]
#Ea  = ncfile.variables['var3'][:,:]
#No= ncfile.variables['var4'][:,:]
##mag  = ncfile.variables['var5'][:,:]
##deg = ncfile.variables['var6'][:,:]
#
## finding indices lat < 0
#la=lat[:][lat <= -1]
#la=la[:][la >= -5]
#nd=np.zeros(len(la))
#k=0
#kk=0
#for x in lat:
#   k=k+1
#   if -5 <= x <= -1:
#     kk=kk+1
#     nd[kk-1]=k-1
#nd=list(nd)
## assigning indices and choose depth 0(0-10m) to 59(590-600m)
#Ea=Ea[nd,0:20]
#No=No[nd,0:20]
#X=lon[nd]
#Y=lat[nd]
#T=time[nd]
#Ea=ma.getdata(Ea)
#No=ma.getdata(No)
#np.savez_compressed("adcp.npz",X=X,Y=Y,Ea=Ea,No=No)
# to load file, uncomment the following lines
npf=np.load("adcp2.npz") #np was numpy
X=npf['X']
Y=npf['Y']
Ea=npf['Ea']
No=npf['No']

print X
print Ea

mag=npf['mag']
deg=npf['deg']

# for Matplotlib, choose a level 0 to 59
U=Ea[:,0]
V=No[:,0]

## removing high values higher than 1 m/s
#from numpy.lib import scimath
#u2=scimath.sqrt(U*U+V*V)
#x=X[nd][u2 < 1000] #X was lon
#y=Y[nd][u2 < 1000] #Y was lat
#u=Ea[:,0][u2 < 1000]
#v=No[:,0][u2 < 1000]
#
#points=np.zeros((len(x),2))
#points[:,0]=x
#points[:,1]=y
#
## gridding (it does not plot)
#X, Y=np.mgrid[184.:190.:40j,-5:-1:20j]
#from scipy.interpolate import griddata
#U = griddata(points, u, (X, Y), method='cubic')
#V = griddata(points, v, (X, Y), method='cubic')

from pylab import *
figure()
Q = quiver( X[::3, ], Y[::3, ], U[::3, ], V[::3, ],
            pivot='mid', color='r', units='inches' )
qk = quiverkey(Q, 0.5, 0.03, 1, r'$1 \frac{m}{s}$', fontproperties={'weight': 'bold'})
plot( X[::3,], Y[::3,], 'k.')
axis([184.5, 190.5, -5, -1])
title("pivot='mid'; every third arrow; units='inches'")
plt.show()
