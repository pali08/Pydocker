'''
========================
3D surface (solid color)
========================

Demonstrates a very basic plot of a 3D surface using a solid color.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def surface(*datasets_list):
    fig = plt.figure()
    #ax=Axes3D(fig3d)
    ax = fig.add_subplot(111, projection='3d')
    #print(datasets_list)
    #for i in range(0, len(datasets_list)):
    #print(datasets_list[i])
    ax.scatter(datasets_list[0][:,0],datasets_list[0][:,1],datasets_list[0][:,2], c="r", marker="o")
    ax.scatter(datasets_list[1][:,0],datasets_list[1][:,1],datasets_list[1][:,2], c="w", marker="o")
    ax.scatter(datasets_list[2][:,0],datasets_list[2][:,1],datasets_list[2][:,2], c="b", marker="^")
    ax.scatter(datasets_list[3][:,0],datasets_list[3][:,1],datasets_list[3][:,2], c="y", marker="^")
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
    #ax.scatter(x, y, z)
    ax.set_xlabel("x axis")
    ax.set_ylabel("y axis")
    ax.set_zlabel("z axis")
    plt.show()
    return(0)
