#/usr/bin/env python3
import sys, os
from align_matrices import align_matrices
from read_bcr_python import read_bcr_header, read_bcr_bin
from read_pdb import read_pdb
from create_folders import create_folder, create_subfolders
import numpy as np
from draw_plot import draw_points
import heapq
'''
def best_fit_find(best_fit, bcr_header, bcr_array, new_corsum_min, old_corsum_min, rots_count, pi_mult):
    old_corsum_min = new_corsum_min
    all_rots, cor_sums, matrices_of_diffs = align_matrices(best_fit, bcr_header, bcr_array, rots_count, pi_mult)
    new_corsum_min_index = cor_sums.index(min(cor_sums))
    new_corsum_min = min(cor_sums)
    pi_mult = pi_mult/2
    best_fit = all_rots[new_corsum_min_index]
    return(best_fit, pi_mult, new_corsum_min, new_corsum_min_index, old_corsum_min, all_rots, cor_sums, matrices_of_diffs)
'''
def compare_and_output(infilename_pdb, infilename_bcr, rots_count, rots_count_around_z, best_fits_count,project_name):
    bcr_array = np.array(read_bcr_bin(infilename_bcr))
    # we put some zeroes around 
    #for i in range(0,5):
        #bcr_array = np.insert(bcr_array,0, values=0, axis=0)
        #bcr_array = np.insert(bcr_array,bcr_array.shape[0], values=0, axis=0)
        #bcr_array = np.insert(bcr_array,0, values=0, axis=1)
        #bcr_array = np.insert(bcr_array,bcr_array.shape[1], values=0, axis=1)
    bcr_header = read_bcr_header(infilename_bcr)
    if(bcr_header["xlength"] / bcr_header["xpixels"] -  bcr_header["ylength"] / bcr_header["ypixels"] < 0.01):
        pixel_size = bcr_header["xlength"] / bcr_header["xpixels"]
    else:
        print("Pixel size has to be the same in x and y direction")
        return(1)
        sys.exit()

    coor_list = read_pdb(infilename_pdb)[1]
    best_fit = coor_list # in first cykle, best fit is default rotation
    list_of_all_rots = []
    create_folder(project_name)
    subfolder = create_subfolders(project_name, "textfiles")
    subfolder_plot = create_subfolders(project_name, "graphs")
    axisangles, cor_sums, diff_matrices, aligned_pdb_matrices, angles_z = align_matrices(coor_list, bcr_header, bcr_array, rots_count, rots_count_around_z)
    #print("Axisangles:")
    #print(axisangles)
    #print("Cor sums:")
    #print(cor_sums)
    #print("Axisangles z")
    #print(axisangles_z)
    #print(len(diff_matrices))
    best_fits = np.argsort(cor_sums)[::1][:best_fits_count]
    #print(best_fits)
    with open(os.path.join(subfolder, "{}_text_output.txt".format(project_name)), mode="w+", encoding='utf-8') as textoutput:
        ind_best = 0
        for i in range(0, len(best_fits)):
            ind_best = best_fits[i]
            glob_rot = ind_best // rots_count_around_z # there are rots_count global * rots_count_around_z rotations we need to know which global rotation give rot_ar_z belongs to
            textoutput.write("score: {} axis {} {} {} angle {} angle around z coor {} \n".format(cor_sums[ind_best],axisangles[glob_rot][0],axisangles[glob_rot][1],axisangles[glob_rot][2],axisangles[glob_rot][3], angles_z[ind_best])) 
            #max_point = np.amax(diff_matrices[ind_best])
            #min_point = np.amin(diff_matrices[ind_best])
            #avg = (max_point + min_point)/2
            draw_points(diff_matrices[ind_best],i,subfolder_plot,cor_sums[ind_best], pixel_size, aligned_pdb_matrices[ind_best], bcr_array)
    return(0)


#graphs_and_textfiles('input_files/1hzh.pdb','input_files/1012_1.bcr', 10, 'myprojectnm5gT') 
