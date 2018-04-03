#!/usr/bin/env python3

import numpy as np
from transform_coordinates import rotate
from read_pdb import read_pdb
import random
#import align_matrices
from read_bcr_python import read_bcr_bin
import transform_coordinates
import math
import sys
from surface3d_demo2 import surface

def get_count_from_angle(angle, count_points_on_cap):
    whole_count = int((2*count_points_on_cap)/(1-np.cos(angle)))
    return(whole_count)

def spiral_dist(angle,count_points_on_cap):
    points_count = get_count_from_angle(angle, count_points_on_cap)
    print(points_count)
    golden_angle = np.pi * (3 - np.sqrt(5))
    theta = golden_angle * np.arange(points_count)
    z = np.linspace(1 - 1.0 / points_count, 1.0 / points_count - 1, points_count)
    radius = np.sqrt(1 - z * z)
    points = np.zeros((count_points_on_cap, 3)) #points equaly distributed on sphere

    for i in range(0, count_points_on_cap):
        points[i,0] = radius[i] * np.cos(theta[i])
        points[i,1] = radius[i] * np.sin(theta[i])
        points[i,2] = z[i]
        #points = points[0:100]
    print(i)
    surface(points[:,0],points[:,1],points[:,2])
    return(0)

spiral_dist(np.pi/4,1000)
