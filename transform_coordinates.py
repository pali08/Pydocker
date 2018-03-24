#!/usr/bin/env python

import math 
import itertools
import numpy as np



def find_center(coord_list):
	x_sum = 0
	y_sum = 0
	z_sum = 0
	for i in range(0,len(coord_list)):
		x_sum = x_sum + coord_list[i][0]
		y_sum = y_sum + coord_list[i][1]
		z_sum = z_sum + coord_list[i][2]
	x_center = x_sum/(len(coord_list))
	y_center = y_sum/(len(coord_list))
	z_center = z_sum/(len(coord_list))
	return x_center, y_center, z_center

def normalize(xyz, tolerance=0.00001):
	#print(xyz)
	xyz = [i*100 for i in xyz]
	mag2 = sum(n * n for n in xyz)
	if abs(mag2 - 1.0) > tolerance:
		mag = np.sqrt(mag2)
		xyz = tuple(n / mag for n in xyz)
	return xyz

#print(normalize([5,3,1], 0.00001))


def q_mult(q1, q2):
	w1, x1, y1, z1 = q1
	w2, x2, y2, z2 = q2
	w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
	x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
	y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
	z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
	return w, x, y, z

#print(q_mult([1,4,5,7],[5,8,9,2]))

def q_conjugate(q):
	w, x, y, z = q
	return (w, -x, -y, -z)

#print(q_conjugate(q_mult([1,4,5,7],[5,8,9,2])))

def qv_mult(q1, v1):
	q2 = (0.0,) + v1
	return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

#print(qv_mult(q_conjugate(q_mult([1,4,5,7],[5,8,9,2])), (1,2,3)))


def axisangle_to_q(phi, axis):
	axis = normalize(axis)
	x, y, z = axis
	phi = phi/2
	w = np.cos(phi)
	x = x * np.sin(phi)
	y = y * np.sin(phi)
	z = z * np.sin(phi)
	return w, x, y, z

#print(axisangle_to_q(np.pi,qv_mult(q_conjugate(q_mult([1,4,5,7],[5,8,9,2])), (1,2,3))))


def rotate_vec(axis_angle, xyz):
	axis = axis_angle[:3]
	phi = axis_angle[3]

	#axis_z = axis_angle_z[:3]
	#phi_z = axis_angle_z[3]

	#for i in range(0,len(axis)):
	#	axis[i] = int(axis[i])
	xyz = tuple(xyz)
	r = axisangle_to_q(phi, axis)
	#r_z = axisangle_to_q(phi_z, axis_z)

	#quat_combo = q_mult(r,r_z)

	new_xyz = qv_mult(r, xyz)

	return new_xyz

#print(rotate_vec(np.pi/4, "0,1,0", [2,0,0]))

#coord_list_a = [[1.0,0.0,0.0], [2.0,0.0,0.0], [3.0,5.0,2.0]]

def rotate(axis_angle, coord_list):
	center_of_rot = find_center(coord_list)
	x_cent = center_of_rot[0]
	y_cent = center_of_rot[1]
	z_cent = center_of_rot[2]
	new_coor_list = []
	#for k in range(0,3):
	#	axis_angle[k] = axis_angle[k] - center_of_rot[k]
	for i in range(0, len(coord_list)):
		new_xyz = ()
		xyz = [0.0,0.0,0.0]
		for j in range(0, len(coord_list[i])):
			#xyz[j] = coord_list[i][j] - center_of_rot[j] 
			xyz[j] = coord_list[i][j]
		new_xyz = rotate_vec(axis_angle, xyz)
		new_xyz = list(new_xyz)
		new_coor_list.append(new_xyz)
	return new_coor_list 
	
#print(rotate(np.pi/4, "0,1,0", coord_list_a))
# posun+rotace v jednom kroku. 
		  
