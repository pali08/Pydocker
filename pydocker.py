#!/usr/bin/env python3
from operator import itemgetter
import urllib.request, urllib.parse, urllib.error
import re
import time
import argparse
import sys

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
from transform_coordinates import rotate
from align_matrices import align_matrices
import read_bcr_python
from compare_and_output import CompareAndOutput

def Main():
    #plt.switch_backend('Qt4Agg') 
    pdb = {}
    parser = argparse.ArgumentParser(description='CryoEM-AFM')
    parser.add_argument("-p","--pdb_files", help = "pdb files to read separated by space", nargs='+', required=True)
    parser.add_argument("-a","--bcr_files", help = "bcr files with header of size 2048 character", nargs='+', required=True)
    parser.add_argument("project_name", help = "folder will be created in current directory in folder docker_output", type=str)
    parser.add_argument("-c","--rots_count", help = "Count of rotations equaly distributed on sphere", type=int, default=1000)
    parser.add_argument("-z","--rots_count_z", help = "Count of rotations around z axis", type=int, default = 20)
    parser.add_argument("-b","--best_fits_count", help = "Count of rotations in every iteration", type=int, default=20)
    parser.add_argument("-r","--refine", help="If set the refinement is done",action="store_true")
    parser.add_argument("--ref_angle", help="Angle for refinement",type=float,default=None)
    parser.add_argument("--ref_docker_rough_output", help="Output file for rough docking",type=str,default=None)
    parser.add_argument("--ref_line_num", help="line num from docker_rough_output", type=int,default=None)
    parser.add_argument("-o","--corner_background", help="size of squares from all 4 corners that will be set as background", \
                        type=int,default=5)
    parser.add_argument("-u","--up_down_step_move", help="If set, the pdb image will be scaled and not moved up or down", \
                        type=int, default=10)
    parser.add_argument("-s","--scale", help="If set, the pdb image will be scaled and not moved up or down", action="store_true")
    
    parser.add_argument("-d","--rmsd", help="If set, score is computed by RMSD, otherwise MAE is used",action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g","--gauss", help="Blur/stretch image with gaussian filter. Argument is followed with sigma value otherwise 0.5 is used as default", \
                       type=float, nargs=2, default=[None,None], metavar='PERIOD')
    group.add_argument("-f","--boxcar", help="Blur/stretch image with boxcar filter. Argument is followed with size of mask otherwise 3 is default (mask size 3x3)", \
                       type=int, nargs='?', const=3, default=None, metavar='PERIOD')
    

    args = parser.parse_args()
    get_results = CompareAndOutput(args.pdb_files, args.bcr_files, args.rots_count, args.rots_count_z, args.best_fits_count, \
                  args.project_name, args.ref_angle, args.ref_docker_rough_output, args.ref_line_num, \
                  args.corner_background, args.up_down_step_move, args.scale,args.refine, args.rmsd, args.gauss, args.boxcar)
    #print(type(args.gauss))
    #print(args.gauss)
    #sys.exit()
    try:
        get_results.compare_and_output_all()
    except KeyboardInterrupt:
        print("The program was interrupted by user")
    return()
if __name__  == '__main__' :
            Main()
