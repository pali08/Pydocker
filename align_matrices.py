#!/usr/bin/env python3
import numpy as np
import os
from read_bcr_python import read_bcr_bin
from pdb_bins import pdb_rots_to_bins 
from draw_plot import draw_points 

def find_highest_point(matrix_gethighest):
	prot_array = matrix_gethighest
	matrix_gethighest = np.array(matrix_gethighest) # create numpy array
	max_value = np.amax(matrix_gethighest) # find highest point in topography
	index_of_max_val = np.argmax(matrix_gethighest) # find index of highest point (one value index -in  matrix of size 4x3  [2,0] is 6, [3,1] is 10 etc.- indexing from 0 )
	array_shape = matrix_gethighest.shape # get shape of array
	indices_of_max_value = np.unravel_index(index_of_max_val, array_shape) # get index of highest value in 2D matrix from 1num index to 2num index 
	return(array_shape, prot_array, indices_of_max_value, max_value)

def check_surrounding(matrix):
	matrix_shape, matrix, ind_max_value, max_value = find_highest_point(matrix)
	circ_diameter = 5 # is treshold- should play around and set good value
	x_max = ind_max_value[0]
	y_max = ind_max_value[1]
	warning_was_writen = False
	max_dist = 5.0 
	for i in range(0, matrix_shape[0]): 
		for j in range(0, matrix_shape[1]): #iterate trough all bcr_array
			if (np.sqrt(((x_max-i)**2)+((y_max-j)**2)) < max_dist): # if value is in circle, do not check it
				continue
			elif(matrix[i][j] < matrix[x_max][y_max] - 1.0 ): # 1.0 is treshold- should play around and set good value, 
				continue #value not in circle but has treshold lesser than we are looking for
			else: # to write warning only once
				return 1
	return 0									
					
#uprav navratovu hodnotu

def align_matrices(coor_list, bcr_header, bcr_array, rots_count, pi_mult):
	pdb_matrices, list_of_all_rots, list_of_axisanles = pdb_rots_to_bins(coor_list, bcr_header, rots_count, pi_mult)	
	#print("Aligning pdb matrices to bcr. This may take some time (or freez/crash computer)")
	#all_rots = pdb_rots_to_bins(infilename_pdb, infilename_bcr)
	#bcr_array = read_bcr_bin(infilename_bcr)
	bcr_array_shape, bcr_array, ind_max_value_bcr, max_val_bcr = find_highest_point(bcr_array)
	x_max_bcr, y_max_bcr = ind_max_value_bcr
	aligned_matrices = []
	korel_sums = []	
	matrices_of_diffs = []
	if (check_surrounding(bcr_array) == 1):
		print("Structure has more highest points- results can be distorted")
	for k in range(0,len(pdb_matrices)): #iterate trough list of matrices 
		pdb_array_shape, pdb_array, ind_max_value_pdb, max_val_pdb = find_highest_point(pdb_matrices[k]) # 
		x_max_pdb, y_max_pdb = ind_max_value_pdb
		x_hp_dist = x_max_bcr - x_max_pdb 
		y_hp_dist = y_max_bcr - x_max_pdb #distances between indices of highest points
		new_pdb_array = np.zeros((bcr_array_shape[0],bcr_array_shape[1])) #new pdb array with shape of bcr array 
		diff_matrix = np.copy(new_pdb_array)
		kor_sum = 0 # set kor_sum to zero and empty shape of 
		try:
			for i in range(0, pdb_array_shape[0]): 
				for j in range(0, pdb_array_shape[1]):
					new_pdb_array[i+x_hp_dist][j+y_hp_dist] = pdb_array[i][j] 
		except IndexError:
			#aligned_matrices.append("Out of range")
			pdb_matrices.remove(pdb_matrices[k])
			list_of_all_rots.remove(pdb_matrices[k])
			list_of_axisangles.remove(list_of_axisangles[k])
			continue
		aligned_matrices.append(new_pdb_array + (max_val_bcr - max_val_pdb))
		for i in range(0, bcr_array_shape[0]):
			for j in range(0, bcr_array_shape[1]):
				kor_sum = kor_sum + abs(bcr_array[i][j] - new_pdb_array[i][j])
				diff_matrix[i][j] = abs(bcr_array[i][j] - new_pdb_array[i][j])
		korel_sums.append(kor_sum)
		matrices_of_diffs.append(diff_matrix)
	#draw_points(bcr_array, aligned_matrices, bcr_array_shape[0], bcr_array_shape[1])
		#print(pdb_array)
	#print(bcr_array)
	print("Aligning pdb matrices to bcr. This may take some time (or freez/crash computer)")
	return(list_of_axisanles, korel_sums, matrices_of_diffs)
	#return(all_rots[0:2])

#print(align_matrices('pyramid.pdb','pyramid.npy'))
#este navrat aj vsetky najlepsie axisangle, aby sme vedeli vypocitat rotaciu oproti povodnemu natoceniu
#pdb_lst = [[1.0,1.0,2.0],[2.0,3.0,5.0],[2.5,3.5,4.5]]
#bcr_array = np.random.rand(128,128)
#print(align_matrices (pdb_lst, {'xlength':100.0, 'ylength':100.0, 'xpixels':128, 'ypixels':128}, bcr_array, 5, 1.0))
#align_matrices([])
