from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from pdb_bins import pdb_to_bins
import os


def fill_coord_lists(prot_matrix): # protein matrix bcr a pdb
	'''
	this function takes count of x, countof y strips and pdb_list. Pdb_to_bins function creates pdb list (format of list described in
	pdb_to_bins function), from which this function creates numpy arrays, which we can then pass to matplotlib to draw
	surface
	'''
	# x_strips and y_strips is count of bins in x and y direction
	# pdb_in_bins_count = pdb_to_bins(infilename_bcr, *pdb_to_draw)
	prot_matrix = np.array(prot_matrix)
	x_bin_count, y_bin_count = prot_matrix.shape 

	x_array = [] 
	y_array = [] #in this array there will be coordinates stored
	z_array = [[0.000 for y in range(0)] for x in range(x_bin_count)] #this creates list of x lists that are empty, so we can use append function in them- we append y numbers, and every number will be z coordinate
	'''
	next two functions fills x and y arrays with int counts of bins
	'''
	for i in range (0,(x_bin_count)): 
		x_array.append(float(i))
	for j in range(0, (y_bin_count)):
		y_array.append(float(j))
	  
	x_array = np.array(x_array) #we have to create np. array (altought it has the same format, meshgrid won`t take it)
	y_array = np.array(y_array)
	y_array, x_array = np.meshgrid(y_array, x_array) 
	#print(x_bin_count)
	#print(y_bin_count)
	#print(len(prot_matrix[0]))
	#print(len(prot_matrix[1])) 
	for k in range(0, (x_bin_count)): #iterate through x bins
		for l in range(0, (y_bin_count)): #iterate trough y bins
			if (abs(prot_matrix[k][l] - 0.000) < 0.0001): #if bin is empty put 0.000 as z coordinate
				z_array[k].append(0.000)
			else:
				z_array[k].append(prot_matrix[k][l]) # else put z coordinate there (which should be the highest coordinate for given bin)
	z_array = np.array(z_array) #again, we have to create numpy array
	return(x_array, y_array, z_array)



def draw_points(diff_matrix, num_of_graph, subfolder, score):
	plt.switch_backend('TkAgg') #default backend is 'agg' and it can only draw png file. I use 'Qt4Agg' for interactive 3D graph. 
	
	#x_ar_bcr, y_ar_bcr, z_ar_bcr = fill_coord_lists(bcr_matrix)
	
	#x_ar_pdb, y_ar_pdb, z_ar_pdb = fill_coord_lists(pdb_matrix)
    
	fig = plt.figure(1)
	'''
	ax = fig.add_subplot(211, projection='3d')
	 
	ax.scatter(x_ar_bcr, y_ar_bcr, z_ar_bcr, color='red')
	ax.scatter(x_ar_pdb, y_ar_pdb, z_ar_pdb, color='green')

	ax.set_xlabel('')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')
	ax.set_title('Correlation score is {}'.format(score))
	'''
	#and now second graph: matrix of differences
	ax2 = fig.add_subplot(211)
	ax2.set_title('Correlation score is {}'.format(score))
	ax2.imshow(diff_matrix)

	graph = os.path.join(subfolder, "{}_graph_{}.png".format(os.path.split(subfolder)[1], num_of_graph))

	plt.savefig(graph)
	plt.close()
	#plt.show()
	return(0)

# TODO: picture name and folder in argument or by joining name of bcr and pdb files

'''
def draw_surface(x_strips, y_strips, *pdb_list_to_draw):
    
    
    #this takes count of x and y bins, pdb_list in format created by pdb_to_bins, makes np arrays (function fill coord list)
    and then draws surface od pdb file
    
    
    arrays = fill_coord_lists(x_strips, y_strips, pdb_list_to_draw)
    
    x_ar = arrays[0]
    y_ar = arrays[1]
    z_ar = arrays[2]

    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x_ar, y_ar, z_ar, cmap=cm.coolwarm, linewidth=0, antialiased=False, rstride=1, cstride=1)
    # Customize the z axis.
    ax.set_zlim(0.0, 60)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
  
    plt.savefig('plot_picture_surface.png')
    return 0
'''
