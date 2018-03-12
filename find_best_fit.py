#/usr/bin/env python3
import sys, os 
from align_matrices import align_matrices
from read_bcr_python import read_bcr_header, read_bcr_bin
from read_pdb import read_pdb
from create_folders import create_folder, create_subfolders
import numpy as np
from draw_plot import draw_points
import heapq

def best_fit_find(best_fit, bcr_header, bcr_array, new_corsum_min, old_corsum_min, rots_count, pi_mult):
	old_corsum_min = new_corsum_min
	all_rots, cor_sums, matrices_of_diffs = align_matrices(best_fit, bcr_header, bcr_array, rots_count, pi_mult)
	new_corsum_min_index = cor_sums.index(min(cor_sums))
	new_corsum_min = min(cor_sums)
	pi_mult = pi_mult/2
	best_fit = all_rots[new_corsum_min_index]
	return(best_fit, pi_mult, new_corsum_min, new_corsum_min_index, old_corsum_min, all_rots, cor_sums, matrices_of_diffs)
	
def compare_and_output(infilename_pdb, infilename_bcr, rots_count, best_fits_count,project_name):
	bcr_array = np.array(read_bcr_bin(infilename_bcr))
	# we put some zeroes around 
	for i in range(0,5):
		bcr_array = np.insert(bcr_array,0, values=0, axis=0)
		bcr_array = np.insert(bcr_array,bcr_array.shape[0], values=0, axis=0)
		bcr_array = np.insert(bcr_array,0, values=0, axis=1)
		bcr_array = np.insert(bcr_array,bcr_array.shape[1], values=0, axis=1)
	bcr_header = read_bcr_header(infilename_bcr)
	num_of_iter = 1
	pi_mult = 2
	coor_list = read_pdb(infilename_pdb)[1]
	best_fit = coor_list # in first cykle, best fit is default rotation
	#all_rots, cor_sums = align_matrices(coor_list, bcr_header, bcr_array, rots_count, pi_mult)	
	#old_corsum_min = 5000000000000.0 
	#new_corsum_min = old_corsum_min - 2 #for first and second cycle float_info.max returns highest available floating point number)
	list_of_all_rots = []
	create_folder(project_name)
	while (a < 1):
		subfolder = create_subfolders(project_name, num_of_iter, "textfiles")
		subfolder_plot = create_subfolders(project_name, num_of_iter, "graphs")
		#best_fit, pi_mult, new_corsum_min, new_corsum_min_index, old_corsum_min, all_rots, cor_sums, matrices_of_diffs = best_fit_find(best_fit, bcr_header, bcr_array, new_corsum_min, old_corsum_min, rots_count, pi_mult)
		axisangles, cor_sums, diff_matrices = align_matrices(coor_list, bcr_header, bcr_array, rots_count, rots_count, pi_mult)
		np.argsort(a)[::1][:heapq.nsmallest(best_fits_count, cor_sums)] #do this after lunch
		best_fits = heapq.nsmallest(best_fits_count, cor_sums)
		with open(os.path.join(subfolder, "{}_{}_text_output.txt".format(project_name, num_of_iter)), mode="w+", encoding='utf-8') as textoutput:
			for i in range(0, len(all_rots)):
				textoutput.write("score:{}_coordinates:{} \n".format(cor_sums[i], all_rots[i]))
				textoutput.write("-----------------------------\n best_score:{}, line: {}".format(new_corsum_min, new_corsum_min_index + 1))
		for j in range(0, len(all_rots)):
			draw_points(bcr_array, best_fit, matrices_of_diffs[j], j, num_of_iter, subfolder, cor_sums[j])	
		num_of_iter = num_of_iter + 1
		print(num_of_iter)
		if (num_of_iter == 10):
			exit()		
		return(best_fit, new_corsum_min)

#graphs_and_textfiles('input_files/1hzh.pdb','input_files/1012_1.bcr', 10, 'myprojectnm5') 
