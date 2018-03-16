#!/usr/bin/env python3
from operator import itemgetter
import urllib.request, urllib.parse, urllib.error
import re
import time
import argparse
from read_pdb import read_pdb
from read_pdb import strip_pdb
from read_bcr_python import read_bcr_header
from rotate import create_rots
#from rotate import first_rot
'''
next two functions compares two values and returns bigger one 
'''
def get_bigger(new_coord, coord):
	biggest_coord = None
	biggest_coord = coord
	if (new_coord > coord):
		biggest_coord = new_coord
	return biggest_coord

def get_smaller(new_coord, coord):
	smallest_coord = None
	smallest_coord = coord
	if (new_coord < coord):
		smallest_coord = new_coord
	return smallest_coord 


#this function finds biggest and smallest x,y or z coordinate from file in format [[x,y,z][x,y,z][x,y,z][x,y,z]]
#its arguments are: pdb list in mentioned file format and coordinate in integer format (coord 0 is x, coord 1 is y coord 2 is z)
def find_biggest_smallest(*pdb_list):

	smallest_x = pdb_list[0][0]
	biggest_x = pdb_list[0][0]
	smallest_y = pdb_list[0][1]
	biggest_y = pdb_list[0][1]
	smallest_z = pdb_list[0][2]
	biggest_z = pdb_list[0][2]
	for i in range(0, len(pdb_list)):
		biggest_x = get_bigger(pdb_list[i][0], biggest_x)
		smallest_x = get_smaller(pdb_list[i][0], smallest_x)
		biggest_y = get_bigger(pdb_list[i][1], biggest_y)
		smallest_y = get_smaller(pdb_list[i][1], smallest_y)
		biggest_z = get_bigger(pdb_list[i][2], biggest_z)
		smallest_z = get_smaller(pdb_list[i][2], smallest_z)
	return biggest_x, smallest_x, biggest_y, smallest_y, biggest_z, smallest_z

#this function puts pdb begin of coordinate system (smallest y will have 0 y coordinate etc)
def pdb_to_000(*pdb_list_to_000): 
		
	#list_of_rots = first_rot(5,5,5,infilename_pdb)
	'''
	this function gets pdb_list in [[x,y,z],[x,y,z]] format and changes their coordinates so, that 
	it shifts them to begin of coordinate system (lowest x will have zero value etc.)
	'''
	#pdb_list_to_000 = read_pdb(infilename_pdb)

	
	pdb_list_000 = []
	zero_coord = find_biggest_smallest(*pdb_list_to_000)
	

	x_in_zero = zero_coord[1]
	y_in_zero = zero_coord[3]
	z_in_zero = zero_coord[5]
  
	x_range = zero_coord[0] - zero_coord[1]
	y_range = zero_coord[2] - zero_coord[3]
	z_range = zero_coord[4] - zero_coord[5]
	
   
	for i in range(0,len(pdb_list_to_000)):
		temp_coord = [] # temporary list coordinate [x,y,z] format
		temp_coord.append(round(pdb_list_to_000[i][0] - (round(x_in_zero, 3)),3)) 
		temp_coord.append(round(pdb_list_to_000[i][1] - (round(y_in_zero, 3)),3))
		temp_coord.append(round(pdb_list_to_000[i][2] - (round(z_in_zero, 3)),3))
		pdb_list_000.append(temp_coord) # append new [x,y,z] to list
	#print zero_coord[0]
	return pdb_list_000, x_range, y_range, z_range


def pdb_to_bins(bin_size ,*pdb_list_to_bins):
	'''
	this function takes pdb in [[x,y,z],[x,y,z]] format and creates list of format:
	2[[z,z,z,z,z][z,z,z,z,z][z,z,z,z,z][z,z,z,z,z][z,z,z,z,z]] count of internal lists is x range, count of numbers in internal list
	is y range and z is z coordinate
	'''
	angstrom2nm = 0.1
	pdb_000_ranges = pdb_to_000(*pdb_list_to_bins) #we save all 4 return values to pdb_000_ranges and then assign particular variables
	
	pdb_000 = pdb_000_ranges[0]
	
	x_rang = pdb_000_ranges[1]
	y_rang = pdb_000_ranges[2]
	z_rang = pdb_000_ranges[3]
	
	count_of_x_strips = int((x_rang*angstrom2nm) / bin_size)+5 #we put 5 bins more to have some surroundings around molecule
	count_of_y_strips = int((y_rang*angstrom2nm)/ bin_size)+5
	pdb_in_bins = [[0.000 for i in range(count_of_y_strips)] for j in range(count_of_x_strips)]

	for k in range(0,len(pdb_000)): #iterate trough all atoms
		x_integerized = int((pdb_000[k][0]*angstrom2nm)/bin_size + 2) # divide x coordinate by bin size and round it to lower number 
		y_integerized = int((pdb_000[k][1]*angstrom2nm)/bin_size + 2) # - int function just tears numbers after decimal point
		if (abs(pdb_in_bins[x_integerized][y_integerized] - 0.000) < 0.0001 ): # if z coordinate equals to 0
			pdb_in_bins[x_integerized][y_integerized] = (pdb_000[k][2])*angstrom2nm # add new z coordinate into list
		elif (int(pdb_000[k][2]) > int(pdb_in_bins[x_integerized][y_integerized])): #if it is not equal, try if it is bigger and if yes, put new (highest) value of z coordinate into bin
			# *1000 and int- this should make every pdb coordinate (3 decimal points) comparable
			pdb_in_bins[x_integerized][y_integerized] = pdb_000[k][2]*angstrom2nm #angstrom2nm 
		else: #if it is smaller continue to next iteration
			continue 
	#print(count_of_x_strips)
	#print(count_of_y_strips)
	#print(bin_size)
	return pdb_in_bins, count_of_x_strips, count_of_y_strips

def pdb_rots_to_bins(coor_list, bcr_header, rots_count, pi_mult):
	#print("Creating 2D matrices from bcr file")
	#bcr_header = read_bcr_header(infilename_bcr)
	if (bcr_header['xlength']/bcr_header['xpixels'] - bcr_header['ylength']/bcr_header['ypixels'] < 0.01) and (not(set(("xunit" and "yunit" and "zunit")).issubset(bcr_header))):
		bin_size = ((bcr_header['xlength']/bcr_header['xpixels'])) 
	rots_list, axisangle_list = create_rots(rots_count, pi_mult ,coor_list)
	pdb_matrices = []
	for i in range(0, len(rots_list)):
		pdb_matrix = pdb_to_bins(bin_size, *rots_list[i])[0]
		pdb_matrices.append(pdb_matrix)
	print("Creating 2D matrices from bcr file")
	return(pdb_matrices, rots_list, axisangle_list)
#pdb_lst = [[1.0,1.0,2.0],[2.0,3.0,5.0],[2.5,3.5,4.5]]
#print(pdb_lst[0][0])
#print(pdb_rots_to_bins (pdb_lst, {'xlength':3.0, 'ylength':3.0, 'xpixels':128, 'ypixels':128}, 5, 1.0))

