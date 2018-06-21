#!/usr/bin/env python3
from operator import itemgetter
import urllib.request, urllib.parse, urllib.error
import re
import time
import argparse

#from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

from read_pdb import read_pdb
from read_pdb import strip_pdb
from pdb_bins import get_bigger
from pdb_bins import get_smaller
from pdb_bins import find_biggest_smallest
from pdb_bins import pdb_to_000
from pdb_bins import pdb_to_bins
from draw_plot import draw_points
#from draw_plot import draw_surface
#from draw_plot import fill_coord_lists
from transform_coordinates import rotate
from align_matrices import align_matrices
import read_bcr_python
from compare_and_output import compare_and_output

def get_res(infilenames_pdb, infilenames_bcr, rots_count, rots_count_around_z, best_fits_count,project_name, refine=False, ref_angle=None, docker_rough_output=None, ref_line_num=None):
    for compare_and_output in get_results:
        return(compare_and_output)
        

def Main():
    #plt.switch_backend('Qt4Agg') 
    pdb = {}
    parser = argparse.ArgumentParser(description='CryoEM-AFM')
    parser.add_argument("-p","--pdb_files", help = "pdb files to read separated by space", type=str, required=True)
    parser.add_argument("-b","--bcr_files", help = "bcr files with header of size 2048 character", type=str, required=True)
    parser.add_argument("project_name", help = "folder will be created in current directory in folder docker_output", type=str)
    parser.add_argument("--rots_count", help = "Count of rotations equaly distributed on sphere", type=int, default=1000)
    parser.add_argument("--rots_count_z", help = "Count of rotations around z axis", type=int, default = 20)
    parser.add_argument("--best_fits_count", help = "Count of rotations in every iteration", type=int, default=20)
    parser.add_argument("--refine", help="If set the refinement is done",action="store_true")
    parser.add_argument("--ref_angle", help="Angle for refinement",type=float,default=None)
    parser.add_argument("--ref_docker_rough_output", help="Output file for rough docking",type=str,default=None)
    parser.add_argument("--ref_line_num", help="line num from docker_rough_output", type=int,default=None)
    args = parser.parse_args()
    get_results = CompareAndOutputAll(args.pdb_file, args.bcr_file, args.rots_count, args.rots_count_z, args.best_fits_count, args.project_name, args.refine, args.ref_angle, args.ref_docker_rough_output, args.ref_line_num)
    def get_res(infilenames_pdb, infilenames_bcr, rots_count, rots_count_around_z, best_fits_count,project_name, refine=False, ref_angle=None, docker_rough_output=None, ref_line_num=None):
        for compare_and_output in get_results:
            return(compare_and_output)
    try:
        get_res(args.pdb_file, args.bcr_file, args.rots_count, args.rots_count_z, args.best_fits_count, args.project_name, args.refine, args.ref_angle, args.ref_docker_rough_output, args.ref_line_num)
    except KeyboardInterrupt:
        print("The program was interrupted by user")
    return()
if __name__  == '__main__' :
            Main()
