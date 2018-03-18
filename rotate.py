import numpy as np 
from transform_coordinates import rotate
from read_pdb import read_pdb
import random
#import align_matrices
from read_bcr_python import read_bcr_bin
import transform_coordinates
import math
import sys
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
	theta = golden_angle * np.arange(n)
	z = np.linspace(1 - 1.0 / points_count, 1.0 / points_count - 1, points_count)
	radius = np.sqrt(1 - z * z)
	points = np.zeros((points_count, 3)) #points equaly distributed on sphere
	rot_axes = np.cross(points,main_ax)
	return(rot_axes, main_ax)

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def axisange_regular(points_count, main_ax):
	rot_axes, main_ax = spiral_dist(points_count, main_ax)
	angle_list = []
    v2_u = unit_vector(main_ax)
	for i in range(0, len(points_count)):
    	v1_u = unit_vector(rot_axes[i])
		angle_list.append(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))) 
	return(rot_axes, angle_list)
	
	
def create_rots(rots_count, pi_mult, coor_list):
	#coor_list = read_pdb(infilename)[1]
	list_of_all_rots = []
	list_of_all_axisangles = []
	reg_axes, reg_angles = axisangle_regular(rots_count, [0,0,1])
	for i in range(0, rots_count):
		#ran_axisangle = ranvec(pi_mult) # it ll became axisangle
		reg_axisangle = reg_axes[i]
		reg_axisangle = reg_axisangle.append(reg_angles[i])
		rotation = rotate(reg_axisangle, coor_list)
		list_of_all_rots.append(rotation)
		list_of_all_axisangles.append(reg_axisangle)

	for i in range(0, len(list_of_all_rots)):
		print("{} {} {}".format(list_of_all_rots[i][0][0], list_of_all_rots[i][0][1], list_of_all_rots[i][0][2]))
	sys.exit()

	return(list_of_all_rots, list_of_all_axisangles)
	
#TODO 3 rotace -> 1 rotace (algoritmus s rovnomernou rotaciou vo v3etkych smeroch
# na skusku: vsetky rotace do 1 grafu -> gula
# nahodna rotace agt overit v nej systematicku rotaciu
