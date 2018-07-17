#!/usr/bin/env python3
import numpy as np
import os
from read_bcr_python import read_bcr_bin
from pdb_bins import pdb_rots_to_bins
from draw_plot import draw_points
from drw_plt_tstng import draw_points_test
import cv2
import sys
from scipy import ndimage
'''
def find_highest_point(matrix_gethighest):
    prot_array = matrix_gethighest
    matrix_gethighest = np.array(matrix_gethighest) # create numpy array
    max_value = np.amax(matrix_gethighest) # find highest point in topography
    index_of_max_val = np.argmax(matrix_gethighest) # find index of highest point (one value index -in matrix
                                                    #of size 4x3  [2,0] is 6, [3,1] is 10 etc.- indexing from 0 )
    array_shape = matrix_gethighest.shape # get shape of array
    indices_of_max_value = np.unravel_index(index_of_max_val, array_shape) # get index of highest value in 2D matrix from 1num index 
                                                                           #to 2num index 
    return(array_shape, prot_array, indices_of_max_value, max_value)

'''
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

def align_matrices(coor_list, bcr_header, bcr_array, rots_count, rots_count_around_z, \
                   docker_rough_output_list=None, \
                   how_much_best_rots=None, \
                   glob_rots_refine=None, z_rots_refine=None,up_down_steps_count, \
                   cb, scale,rmsd ,gauss, boxcar_size): # cb is corner background

    def autorefine(first_x_structures, glob_rot_ref, z_rot_ref)
        cap_surface = 4*np.pi/rots_count
        angle_ref_glob = 1-(cap_surface/(2*np.pi))
        angle_ref_z = 2*np.pi / rots_count_z
    
    avg_background1 = np.sum(bcr_array[bcr_array.shape[0]-cb:bcr_array.shape[0],bcr_array.shape[1]-cb:bcr_array.shape[1]])/cb**2
    avg_background2 = np.sum(bcr_array[bcr_array.shape[0]-cb:bcr_array.shape[0],:cb])/cb**2
    avg_background3 = np.sum(bcr_array[:cb,bcr_array.shape[1]-cb:bcr_array.shape[1]])/cb**2
    avg_background4 = np.sum(bcr_array[:cb,:cb])/cb**2
    avg_backgrounds = [avg_background1,avg_background2, avg_background3, avg_background4]
    avg_background = (np.sum(bcr_array[bcr_array.shape[0]-cb:bcr_array.shape[0],bcr_array.shape[1]-cb:bcr_array.shape[1]]) + \
                      np.sum(bcr_array[bcr_array.shape[0]-cb:bcr_array.shape[0],:cb]) + np.sum(bcr_array[:cb,bcr_array.shape[1]-cb:bcr_array.shape[1]]) + \
                      np.sum(bcr_array[:cb,:cb]))/(4*cb*cb)
    print(avg_backgrounds)
    print(avg_background)
    if (all(abs(1-(i/avg_background)) <= 0.35 for i in avg_backgrounds)==False):
        print("The afm image is in the corner or you set too small -o parameter where background size vary in big range. Try to crop image with bigger background or set bigger -o parameter")
        sys.exit()
    #avg_bck_count = 4*cb*cb
    #sys.exit()
    pdb_matrices, list_of_all_rots, list_of_axisangles, list_of_all_angles_z, axisangles_complete= pdb_rots_to_bins(coor_list, bcr_header, rots_count, rots_count_around_z, docker_rough_output_list, how_much_best_rots,glob_rots_refine, z_rots_refine)
    bcr_array = np.array(bcr_array)
    #print(bcr_array)
    mat2_afm_max = bcr_array.max()
    mat2_afm_min = bcr_array.min()

    mat2_afm_range = mat2_afm_max - avg_background
    def get_max_min_range(mat1_pdb):
        mat1_pdb_max = mat1_pdb.max()
        mat1_pdb_min = mat1_pdb.min()
        mat1_pdb_range = mat1_pdb_max - mat1_pdb_min
        return (mat1_pdb_max, mat1_pdb_min, mat1_pdb_range)
    def scale_matrices(mat1_pdb):
        p1max,p1min,p1range = get_max_min_range(mat1_pdb)
        mat1_pdb = avg_background + ((mat2_afm_range)*((mat1_pdb-p1min)/(p1range))) # resp. miesto min tam moze ist average background
        min_val,top_left = opencv_align(bcr_array,mat1_pdb)
        return(top_left,mat1_pdb) # p1min will be the 
    def move_up_down(mat1_pdb):
        p1max,p1min,p1range = get_max_min_range(mat1_pdb)
        bol_pdb = mat1_pdb > 0.01 # I guess, that 1/10 Angstrom is biggest value I care about
        mat1_pdb = mat1_pdb + avg_background # pdb must be with zero backgroud
        step = (mat2_afm_max-p1max)/up_down_steps_count
        l = 0
        #bol_pdb = abs(mat1_pdb - avg_background) > 0.0001 # all background pixels set to 0 (False), non background px are 1 (true)
        #print(bol_pdb)
        score_new = sys.maxsize-1 # maximal available integer
        score_old = sys.maxsize
        mat1_pdb_mov = mat1_pdb
        while l <= up_down_steps_count and score_new < score_old:
            score_old = score_new
            mat1_pdb_mov_old = mat1_pdb_mov
            mat1_pdb_mov = mat1_pdb + bol_pdb*l*step # lever up only non background pixels (bol pdb is bolean matrix- 1for pixels > average)
            score_new,top_left = opencv_align(bcr_array,mat1_pdb_mov) # after levering up, we need to align
            l = l+1
        return(top_left, mat1_pdb_mov_old) # old pdb will have lower score than new one

    aligned_matrices = []
    korel_sums = []
    matrices_of_diffs = []
    gauss_1 = int(gauss[1])
    print("Aligning pdb matrices to bcr.")
    for k in range(0,len(pdb_matrices)): #iterate trough list of matrices 

        pdb_array = np.array(pdb_matrices[k])
        pdb_array_shape = pdb_array.shape
        #maska2 = pdb_array_with_surroundings > 0.000
        #maska2 = maska2*100
        #pdb_array_new = pdb_array_with_surroundings[np.ix_(maska2.any(1),maska2.any(0))]
        #draw_points_test(pdb_array_new,"{}_pdb_array_new.png".format(str(k)))
        if(not(gauss == [None,None])):
            #pdb_array = ndimage.gaussian_filter(pdb_array_with_surroundings, gauss_sigma, order=0)
            pdb_array_with_surroundings = np.full((pdb_array_shape[0]+((int(gauss_1)-1)*2),pdb_array_shape[1]+((int(gauss_1)-1)*2)),0.000)
            pdb_array_with_surroundings[int(gauss_1-1): pdb_array_shape[0]+gauss_1-1, \
                                        int(gauss_1-1): pdb_array_shape[1]+gauss_1-1] = pdb_array
            pdb_array=cv2.GaussianBlur(pdb_array_with_surroundings,ksize=(gauss_1,gauss_1),sigmaX=gauss[0],sigmaY=0,borderType=cv2.BORDER_CONSTANT)
            #cropp
            draw_points_test(pdb_array,"{}_gauss".format(str(k)))
            #mask = pdb_array > 0.0001 # for zeroes true, for non zeroes false
            #pdb_array = pdb_array[np.ix_(mask.any(1),mask.any(0))]
        elif(boxcar_size is not None):
            pdb_array_with_surroundings = np.full((pdb_array_shape[0]+((int(boxcar_size)-1)*2),pdb_array_shape[1]+((int(boxcar_size)-1)*2)),0.000)
            pdb_array_with_surroundings[int(boxcar_size-1): pdb_array_shape[0]+boxcar_size-1, \
                                        int(boxcar_size-1): pdb_array_shape[1]+boxcar_size-1] = pdb_array
            #pdb_array = ndimage.uniform_filter(pdb_array_with_surroundings, boxcar_size)
            pdb_array = cv2.boxFilter(pdb_array_with_surroundings,ksize=(boxcar_size,boxcar_size),borderType=cv2.BORDER_CONSTANT, ddepth=-1)
            draw_points_test(pdb_array,"{}_poboxcar".format(str(k)))
            #cropp
            #mat_for_crop = (1000000000*pdb_array).astype(np.uint8)
            #mask = pdb_array > 0.0001 # for zeroes true, for non zeroes false
            #draw_points_test(mask,"{}_maska_furttonejde.png".format(str(k)))
            #mask = mask*100
            #pdb_array = pdb_array[np.ix_(mask.any(1),mask.any(0))]

        pdb_array_shape = pdb_array.shape
        max_val_pdb = np.amax(pdb_array)
        kor_sum = 0
        if scale==True:
            try:
                yx_dist, pdb_array = scale_matrices(pdb_array)
                y_dist, x_dist = yx_dist
            except cv2.error as e:
                print("Cv2 error")
                korel_sums.append(sys.float_info.max)
                matrices_of_diffs.append(np.full(bcr_array.shape, sys.float_info.max/2))
                aligned_matrices.append(np.full(bcr_array.shape, sys.float_info.max/2))
                continue
        else:
            try:
                yx_dist, pdb_array = move_up_down(pdb_array)
                y_dist, x_dist = yx_dist
            except cv2.error as e:
                print("Cv2 error")
                korel_sums.append(sys.float_info.max)
                matrices_of_diffs.append(np.full(bcr_array.shape, sys.float_info.max/2))
                aligned_matrices.append(np.full(bcr_array.shape, sys.float_info.max/2))
                continue
        new_pdb_array = np.full((bcr_array.shape[0],bcr_array.shape[1]),avg_background) #new pdb array with shape of bcr array 
        diff_matrix = np.copy(new_pdb_array)
        try:
            new_pdb_array[x_dist : x_dist + pdb_array_shape[0], y_dist : y_dist + pdb_array_shape[1]] = pdb_array
        except (IndexError,ValueError):
            print("Index error or value error- if there are many of these outputs, the input bcr matrix is probably too small")
            continue
        aligned_matrices.append(new_pdb_array)
        if (rmsd == False):
            diff_matrix = abs(bcr_array - new_pdb_array)
            kor_sum = diff_matrix.sum()/bcr_array.size
        else:
            diff_matrix = np.sqrt((bcr_array-new_pdb_array)**2)
            kor_sum = diff_matrix.sum()/np.sqrt(bcr_array.size)
        korel_sums.append(kor_sum)
        matrices_of_diffs.append(diff_matrix)
    #sys.exit()
    return(list_of_axisangles, korel_sums, matrices_of_diffs, aligned_matrices, list_of_all_angles_z, axisangles_complete)
