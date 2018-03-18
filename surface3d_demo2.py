'''
========================
3D surface (solid color)
========================

Demonstrates a very basic plot of a 3D surface using a solid color.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def surface(x,y,z):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	# Make data
	#u = np.linspace(0, 2 * np.pi, 100)
	#v = np.linspace(0, np.pi, 100)
	#x = 10 * np.outer(np.cos(u), np.sin(v))
	#y = 10 * np.outer(np.sin(u), np.sin(v))
	#z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))
	#x,y,z = np.meshgrid(x,y,z)
	#print(x)
	#print(z)
	# Plot the surface
	ax.scatter(x, y, z)
	plt.show()
	return(0)
