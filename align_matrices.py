#!/usr/bin/env python3
import numpy as np
import os
from read_bcr_python import read_bcr_bin
from pdb_bins import pdb_rots_to_bins
from draw_plot import draw_points
import cv2
import sys

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

def opencv_align(bcr_array,pdb_array):

    bcr = bcr_array.astype(np.float32)
    bcr2 = bcr.copy()
    template = pdb_array.astype(np.float32)
    w, h = template.shape[::-1]

    bcr = bcr2.copy()

    # Apply template Matching
    res = cv2.matchTemplate(bcr,template,1)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    return(min_val,top_left)

def align_matrices(coor_list, bcr_header, bcr_array, rots_count, rots_count_around_z,scale,refine, ref_angle, docker_rough_output, ref_line_num):
    pdb_matrices, list_of_all_rots, list_of_axisangles, list_of_all_angles_z = pdb_rots_to_bins(coor_list, bcr_header, rots_count, rots_count_around_z, refine, ref_angle, docker_rough_output, ref_line_num)
    def get_max_min_range(mat1_pdb, mat2_afm):
        mat1_pdb_max = mat1_pdb.max()
        mat1_pdb_min = mat1_pdb.min()
        mat2_afm_max = mat2_afm.max()
        mat2_afm_min = mat2_afm.min()
        mat2_afm_range = mat2_afm_max - mat2_afm_min
        mat1_pdb_range = mat1_afm_max - mat1_afm_min
        return (mat1_pdb_max, mat1_pdb_min, mat2_afm_max, mat2_afm_min, mat1_pdb_range, mat2_afm_range)
    def scale_matrices(mat1_pdb, mat2_afm):
            p1max,p1min,a2max,a2min,p1range,a2range = get_max_min_range(mat1_pdb,mat2_afm)
            mat1_pdb = a2min + ((a2range)*((mat1_pdb-p1min)/(p1range)))
        return(mat1_pdb, mat2_afm)
    def move_up_down(mat1_pdb, mat2_afm, best_found_po):
        p1max,p1min,a2max,a2min,p1range,a2range = get_max_min_range(mat1_pdb,mat2_afm)
        avg_background = sum(np.sum(bcr_array[bcr_array.shape[0]-5:bcr_array.shape[0],bcr_array.shape[1]-5:bcr_array.shape[1]]) + \ 
        np.sum(bcr_array[bcr_array.shape[0]-5:bcr_array.shape[0],:5) + np.sum(bcr_array[:5,bcr_array.shape[1]-5:bcr_array.shape[1]]) + \ 
        np.sum(bcr_array[:5,:5]))/100
        mat1_pdb = mat1_pdb + avg_background # pdb must be with zero backgroud
        if (p1range < a2range):
            step = (a2max - p1max)/10
            l = 0
            score_new = sys.maxsize-1 # maximal available integer
            score_old = sys.maxsize
            while l < 10 and score_new < score_old:
                score_old = score_new
                bol_pdb = abs(mat1_pdb - avg_background) < 0.0001
                mat1_pdb = mat1_pdb + bol_pdb*l*step # lever up only non background pixels (bol pdb is bolean matrix- 1for pixels > average)
                score_new,topleft = opencv_align(mat2_afm,mat1_pdb) # after levering up, we need to align
        elif (p1range > a2range):
            step = (p1max - a2max)/10
            l = 0
            score_new = sys.maxsize-1
            score_old = sys.maxsize
            while l<10 and score_new < score_old:
                score old = score_new # continue here


    bcr_array = np.array(bcr_array)
    avg_background = sum(np.sum(bcr_array[bcr_array.shape[0]-5:bcr_array.shape[0],bcr_array.shape[1]-5:bcr_array.shape[1]]) + np.sum(bcr_array[bcr_array.shape[0]-5:bcr_array.shape[0],:5) + np.sum(bcr_array[:5,bcr_array.shape[1]-5:bcr_array.shape[1]]) + np.sum(bcr_array[:5,:5]))/100
    #bcr_array_shape = bcr_array.shape
    max_val_bcr = np.amax(bcr_array) # find highest point in topography
    aligned_matrices = []
    korel_sums = []
    matrices_of_diffs = []
    if (check_surrounding(bcr_array) == 1):
        print("Structure has more highest points- results can be distorted")
    print("Aligning pdb matrices to bcr.")
    for k in range(0,len(pdb_matrices)): #iterate trough list of matrices 

        pdb_array = np.array(pdb_matrices[k])
        pdb_array_shape = pdb_array.shape
        max_val_pdb = np.amax(pdb_array)
        max_val = max_val_bcr - max_val_pdb
        kor_sum = 0
        try:
            y_dist, x_dist = opencv_align(bcr_array, pdb_array)
        except cv2.error as e:
            #print("Cv2 error")
            korel_sums.append(sys.float_info.max)
            matrices_of_diffs.append(np.full(bcr_array.shape, sys.float_info.max/2))
            aligned_matrices.append(np.full(bcr_array.shape, sys.float_info.max/2))
            continue
        new_pdb_array = np.zeros((bcr_array.shape[0],bcr_array.shape[1])) #new pdb array with shape of bcr array 
        diff_matrix = np.copy(new_pdb_array)
        try:
            #for i in range(0, pdb_array_shape[0]):
            #for j in range(0, pdb_array_shape[1]):
            #if(i+x_dist >= 0 and j+y_dist >= 0):
            new_pdb_array[x_dist : x_dist + pdb_array_shape[0], y_dist : y_dist + pdb_array_shape[1]] = pdb_array
            #else:
            #raise IndexError("")
            #print(new_pdb_array)
        except IndexError:
            print("Index error")
            continue
        new_pdb_array = new_pdb_array + max_val

        aligned_matrices.append(new_pdb_array)
        diff_matrix = abs(bcr_array - new_pdb_array)
        kor_sum = diff_matrix.sum()/bcr_array.size
        korel_sums.append(kor_sum)
        matrices_of_diffs.append(diff_matrix)
    return(list_of_axisangles, korel_sums, matrices_of_diffs, aligned_matrices, list_of_all_angles_z)
'''
moving image up and down not done yet

or i in range(0,10): # moving pdb up and down (lowest : backgrounds, highest:highest points)
it = np.nditer(pdb_array, flags=['multi_index'])
while not it.finished:
if(not(abs(pdb_array[it.multi_index[0],it.multi_index[1]] - avg_background)<0.0001)):
pdb_array[it.multi_index[0],it.multi_index[1]] = pdb_array[it.multi_index[0],it.multi_index[1]] + max_val/10*i
'''
