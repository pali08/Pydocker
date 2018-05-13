#/usr/bin/env python3
import sys, os
from align_matrices import align_matrices
from read_bcr_python import read_bcr_header, read_bcr_bin
from read_pdb import read_pdb
#from create_folders import create_folder, create_subfolders
import numpy as np
from draw_plot import draw_points
import heapq
from create_folders import CreateFolder
from create_folders import CreateFolderRefine
import transform_coordinates
import linecache

def compare_and_output(infilename_pdb, infilename_bcr, rots_count, rots_count_around_z, best_fits_count,project_name, refine=False, ref_angle=None, docker_rough_output=None, ref_line_num=None):
    bcr_array = np.array(read_bcr_bin(infilename_bcr))
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
    if((refine is False) and (ref_angle is None) and (docker_rough_output is None)):
        create_folders_object = CreateFolder(project_name, "textfile")
    elif(refine is True and (ref_angle is not None) and (docker_rough_output is not None)):
        create_folders_object = CreateFolderRefine(project_name, "textfile", ref_line_num)

    create_folders_object.create_folder()
    #create_folders_object.plot_or_text = "textfile"
    subfolder = create_folders_object.create_subfolders()
    create_folders_object.plot_or_text = "graphs"
    subfolder_plot = create_folders_object.create_subfolders()

    axisangles, cor_sums, diff_matrices, aligned_pdb_matrices, angles_z = align_matrices(coor_list, bcr_header, bcr_array, rots_count, rots_count_around_z, refine, ref_angle, docker_rough_output, ref_line_num)
    best_fits = np.argsort(cor_sums)[::1][:best_fits_count]
    if (refine == True):
        line_cg = linecache.getline(docker_rough_output,ref_line_num).split()
        line_cg_axis = [float(line_cg[3]),float(line_cg[4]),float(line_cg[5])]
        line_cg_angle = float(line_cg[7])
        q_cg = transform_coordinates.axisangle_to_q(line_cg_angle,line_cg_axis)
    with open(os.path.join(subfolder, "{}_text_output.txt".format(project_name)), mode="w+", encoding='utf-8') as textoutput:
        ind_best = 0
        for i in range(0, len(best_fits)):
            ind_best = best_fits[i]
            glob_rot = ind_best // rots_count_around_z # there are rots_count global * rots_count_around_z rotations we need to know which global rotation give rot_ar_z belongs to
            q_global = transform_coordinates.axisangle_to_q(axisangles[glob_rot][3],[axisangles[glob_rot][0],axisangles[glob_rot][1],axisangles[glob_rot][2]])
            q_z = transform_coordinates.axisangle_to_q(angles_z[ind_best],[0,0,1])
            q_glob_z = transform_coordinates.q_mult(q_z,q_global)
            if(refine == True):
                q_glob_z = transform_coordinates.q_mult(q_glob_z,q_cg)
            axisangle_for_output = transform_coordinates.q_to_axisangle(q_glob_z)
            textoutput.write("score: {0:.3f} axis: {1:.5f} {2:.5f} {3:.5f} angle: {4:.5f} \n".format(cor_sums[ind_best],axisangle_for_output[0],axisangle_for_output[1],axisangle_for_output[2],axisangle_for_output[3]))
            draw_points(diff_matrices[ind_best],i,subfolder_plot,cor_sums[ind_best], pixel_size, aligned_pdb_matrices[ind_best], bcr_array)
    return(0)


