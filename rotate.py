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
'''
def first_rot(x_rotations_count, y_rotations_count, z_rotations_count, pdb_file):
    coord_list = read_pdb(pdb_file)[1]
    y_turn_angle = (2*np.pi)/y_rotations_count
    x_turn_angle = (2*np.pi)/x_rotations_count
    z_turn_angle = (2*np.pi)/x_rotations_count
    list_of_all_rots=[]
    for i in range(0,x_rotations_count):
        coor_list_x_rot = rotate(x_turn_angle*i,"1,0,0", *coord_list)
        for j in range(0, y_rotations_count):
            coor_list_y_rot = rotate(y_turn_angle*j, "0,1,0", *coor_list_x_rot)
            for k in range(0, z_rotations_count):
                coor_list_final_rot = rotate(z_turn_angle*k, "0,0,1", *coor_list_y_rot)
                list_of_all_rots.append(coor_list_final_rot)

    return(list_of_all_rots)
'''
def ranvec(pi_mult):
    #coord_list = read_pdb(pdb_file)[1]
    #list_of_all_rots = []
    a = 2
    while(a > 1.0):
        xi1 = 1.0 - (2.0*random.random())
        xi2 = 1.0 - (2.0*random.random())
        a = (xi1*xi1) - (xi2*xi2)
    b = 2.0*math.sqrt(1-a)
    x_ranvec = xi1*b
    y_ranvec = xi2*b
    z_ranvec = 1.0 - (2.0*a)
    ran_angle = random.random()*(pi_mult*math.pi)
    return(x_ranvec, y_ranvec, z_ranvec, ran_angle)

def spiral_dist(points_count, main_ax):
    golden_angle = np.pi * (3 - np.sqrt(5))
    theta = golden_angle * np.arange(points_count)
    z = np.linspace(1 - 1.0 / points_count, 1.0 / points_count - 1, points_count)
    radius = np.sqrt(1 - z * z)
    points = np.zeros((points_count, 3)) #points equaly distributed on sphere
    points[:,0] = radius * np.cos(theta)
    points[:,1] = radius * np.sin(theta)
    points[:,2] = z
    #rot_axes = np.cross(points,main_ax)
    rot_axes = [[] for i in range(0, len(points))]
    for i in range(0, len(points)):
        rot_axes[i] = np.cross(points[i], main_ax)
    print(rot_axes)
    rot_axes = np.array(rot_axes)
    #surface(points[:,0],points[:,1],points[:,2])
    #sys.exit()
    #print("these are rot axes")
    #print(rot_axes) 
    #print("eorotaxes")
    return(rot_axes, points, main_ax)

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    #print(vector)
    return vector / np.linalg.norm(vector)

def axisangle_regular(points_count, main_ax):
    rot_axes, points, main_ax= spiral_dist(points_count, main_ax)
    angle_list = []
    v2_u = unit_vector(main_ax)
    for i in range(0, points_count):
        v1_u = unit_vector(points[i])
        angle_list.append((np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))))
    #print(angle_list)
    return(rot_axes, angle_list)


def create_rots(rots_count, pi_mult, coor_list):
    #coor_list = read_pdb(infilename)[1]
    rots_count_all_dirs = int(rots_count/10)
    rots_count_z_dir = 10
    list_of_all_rots = []
    #list_of_all_axisangles = [[] for n in range(0,rots_count_all_dirs*rots_count_z_dir)]
    list_of_all_axisangles = []
    reg_axes, reg_angles = axisangle_regular(rots_count_all_dirs, [0.0,0.0,1.0])
    #print(reg_axes)
    #print(reg_angles)
    surface_xyz = []
    reg_axisangle = []
    angle_step = (2*np.pi)/rots_count_z_dir
    reg_axisangle_z = [[0.0,0.0,1.0,k*angle_step] for k in range(rots_count_z_dir*rots_count_all_dirs)]
    for i in range(0, rots_count_all_dirs):
        #for j in range(0, rots_count_z_dir):
        reg_axisangle = np.append(reg_axes[i], reg_angles[i])
        #print(reg_axisangle)
        rotation = rotate(reg_axisangle, coor_list)
        #print(rotation[0])
        list_of_all_rots.append(rotation)
        list_of_all_axisangles.append(reg_axisangle)
        surface_xyz.append((rotation[0]))
    #for i in range(0, len(list_of_all_rots)):
        #print("{} {} {}".format(list_of_all_axisangles[i][0], list_of_all_axisangles[i][1], list_of_all_axisangles[i][2]))
    x = np.array([item[0] for item in surface_xyz])
    y = np.array([item[1] for item in surface_xyz])
    z = np.array([item[2] for item in surface_xyz])
    #surface(x,y,z)
    #sys.exit()

    return(list_of_all_rots, list_of_all_axisangles, reg_axisangle_z)


def rotate_around_z(rots_count_z, coor_list):
    angle = (2*np.pi)/rots_count_z
    rot_angles = [i*angle for i in range(0,rots_count)]
    new_coor_lists = []
    for i in range(0, rots_count_z):
        new_coor_list = rotate([0,0,1,rot_angles[z]], coor_list)
        new_coor_lists.append(new_coor_list)
    return(new_coor_lists)

#TODO 3 rotace -> 1 rotace (algoritmus s rovnomernou rotaciou vo v3etkych smeroch
# na skusku: vsetky rotace do 1 grafu -> gula
# nahodna rotace agt overit v nej systematicku rotaciu
