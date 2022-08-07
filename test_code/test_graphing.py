import matplotlib.pyplot as plt
import matplotlib.colors as clr
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#X_tri = [1,2,4,8]
#Y_tri = [1,7,5,3]
#Z_tri = [1,2,4,3]
#ax.plot_trisurf(X_tri, Y_tri, Z_tri)

X_quiv = [1,5,9]
Y_quiv = [4,3,7]
Z_quiv = [10,6,2]
U_quiv = [3,1,10]
V_quiv = [1,1,20]
# W = Z
W_quiv = [0,0,0] # to keep only cardinal directions

#ax.quiver(X_quiv, Y_quiv, Z_quiv, U_quiv, V_quiv, W_quiv, colors = ['g'])

c = ['g','r','b']
#l = [1,2,2]

for i in range(0,len(X_quiv)):
	ax.quiver(X_quiv[i], Y_quiv[i], Z_quiv[i], U_quiv[i], V_quiv[i], W_quiv[i], colors = c[i]) #length = l[i],

plt.show()