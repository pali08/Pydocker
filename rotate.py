import numpy as np 
from transform_coordinates import rotate
from read_pdb import read_pdb
import random
#import align_matrices
from read_bcr_python import read_bcr_bin
import transform_coordinates
import math
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
		
def create_rots(rots_count, pi_mult, coor_list):
	#coor_list = read_pdb(infilename)[1]
	list_of_all_rots = []
	list_of_all_axisangles = []
	for i in range(0, rots_count):
		ran_axisangle = ranvec(pi_mult) # it ll became axisangle
		rotation = rotate(ran_axisangle, coor_list)
		list_of_all_rots.append(rotation)
		list_of_all_axisangles.append(ran_axisangle)
	return(list_of_all_rots, list_of_all_axisangles)
	
#TODO 3 rotace -> 1 rotace (algoritmus s rovnomernou rotaciou vo v3etkych smeroch
# na skusku: vsetky rotace do 1 grafu -> gula
# nahodna rotace agt overit v nej systematicku rotaciu
