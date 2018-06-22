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
import pathlib



class CompareAndOutput(object):
    def __init__(self, infilenames_pdb, infilenames_bcr, rots_count, rots_count_around_z, best_fits_count,project_name, refine=False, ref_angle=None, docker_rough_output=None, ref_line_num=None):
        self.infilenames_pdb = infilenames_pdb
        self.infilenames_bcr = infilenames_bcr
        self.rots_count = rots_count
        self.rots_count_around_z = rots_count_around_z
        self.best_fits_count = best_fits_count
        self.project_name = project_name
        self.refine = refine
        self.ref_angle = ref_angle
        self.docker_rough_output = docker_rough_output
        self.ref_line_num = ref_line_num
 
    def compare_and_output(self, infilename_pdb, infilename_bcr):
        self.infilename_pdb = infilename_pdb
        self.infilename_bcr = infilename_bcr
        bcr_array = np.array(read_bcr_bin(self.infilename_bcr))
        bcr_header = read_bcr_header(self.infilename_bcr)
        if(bcr_header["xlength"] / bcr_header["xpixels"] -  bcr_header["ylength"] / bcr_header["ypixels"] < 0.01):
            pixel_size = bcr_header["xlength"] / bcr_header["xpixels"]
        else:
            print("Pixel size has to be the same in x and y direction")
            return(1)
            sys.exit()
    
        coor_list = read_pdb(self.infilename_pdb)[1]
        best_fit = coor_list # in first cykle, best fit is default rotation
        list_of_all_rots = []
        if((self.refine is False) and (self.ref_angle is None) and (self.docker_rough_output is None)):
            create_folders_object = CreateFolder(self.infilename_pdb, self.infilename_bcr, self.project_name)
        elif(self.refine is True and (self.ref_angle is not None) and (self.docker_rough_output is not None)):
            create_folders_object = CreateFolderRefine(self.infilename_pdb, self.infilename_bcr, self.project_name, self.ref_line_num)
        folder = create_folders_object.create_folder()
    
        axisangles, cor_sums, diff_matrices, aligned_pdb_matrices, angles_z = align_matrices(coor_list, bcr_header, bcr_array, self.rots_count, self.rots_count_around_z, self.refine, self.ref_angle, self.docker_rough_output, self.ref_line_num)
        best_fits = np.argsort(cor_sums)[::1][:self.best_fits_count]
        if (self.refine == True):
            line_cg = linecache.getline(self.docker_rough_output,self.ref_line_num).split()
            line_cg_axis = [float(line_cg[3]),float(line_cg[4]),float(line_cg[5])]
            line_cg_angle = float(line_cg[7])
            q_cg = transform_coordinates.axisangle_to_q(line_cg_angle,line_cg_axis)
        with open(str(pathlib.Path(folder, "text_output.txt")), mode="w+", encoding='utf-8') as textoutput:
            textoutput.write("Pydocker output\nPdb_file: {}\nBcr file: {}\nGlobal rotations: {}\nZ rotations: {}\nRefinement: {}\nRef. line number: {}\nRef. angle: {}\n".format(infilename_pdb, infilename_bcr, self.rots_count, self.rots_count_around_z, str(self.refine), str(self.ref_line_num), str(self.ref_angle)))
            ind_best = 0
            for i in range(0, len(best_fits)):
                ind_best = best_fits[i]
                glob_rot = ind_best // self.rots_count_around_z # there are rots_count global * rots_count_around_z rotations we need to know which global rotation give rot_ar_z belongs to
                q_global = transform_coordinates.axisangle_to_q(axisangles[glob_rot][3],[axisangles[glob_rot][0],axisangles[glob_rot][1],axisangles[glob_rot][2]])
                q_z = transform_coordinates.axisangle_to_q(angles_z[ind_best],[0,0,1])
                q_glob_z = transform_coordinates.q_mult(q_z,q_global)
                if(self.refine == True):
                    q_glob_z = transform_coordinates.q_mult(q_glob_z,q_cg)
                axisangle_for_output = transform_coordinates.q_to_axisangle(q_glob_z)
                textoutput.write("score: {0:.3f} axis: {1:.5f} {2:.5f} {3:.5f} angle: {4:.5f} \n".format(cor_sums[ind_best],axisangle_for_output[0],axisangle_for_output[1],axisangle_for_output[2],axisangle_for_output[3]))
                draw_points(diff_matrices[ind_best],i,folder,cor_sums[ind_best], pixel_size, aligned_pdb_matrices[ind_best], bcr_array)
        '''
        if (refine == False):
            with open(os.path.join(subfolder, "text_output_global_z_indiv.txt"), mode="w+", encoding='utf-8') as textoutput2:
                for i in range(0, len(best_fits)):
                    ind_best = best_fits[i]
                    glob_rot = ind_best // rots_count_around_z # there are rots_count global * rots_count_around_z rotations we need to know which global rotation give rot_ar_z belongs to
                    textoutput2.write("score: {} axis: {} {} {} angle: {} angle_around_z_coor: {} \n".format(cor_sums[ind_best],axisangles[glob_rot][0],axisangles[glob_rot][1],axisangles[glob_rot][2],axisangles[glob_rot][3], angles_z[ind_best]))
        '''
    def compare_and_output_all(self):
        
        for p in self.infilenames_pdb:
            for b in self.infilenames_bcr:
                self.compare_and_output(p,b)
        return(0)



