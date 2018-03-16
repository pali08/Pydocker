#!/usr/bin/env python3
import numpy as np
import os

def create_bcr_header(line, header_dict):
	line_splitted = line.split(sep=" = ")
	bcr_param = line_splitted[0].strip()

	bcr_value = float(line_splitted[1].strip().replace(",", ""))
	header_dict[bcr_param] = bcr_value



def read_bcr_header(infilename):
	print("Reading header part of bcr file")
	header_dict = {}
	with open(infilename, encoding='utf-8', errors='ignore') as bcr_file:
		line_num = 0
		for line in bcr_file:
			if (line.startswith(("#","%"))):
				continue # ignore comments
			if line.startswith('fileformat'):
				line_splitted = line.split(sep=" = ")
				bcr_param = line_splitted[0].strip() # parameter from bcr file
				bcr_value = line_splitted[1].strip() # value of that parameter
			if line.startswith(('headersize','xpixels','ypixels','xlength','ylength','current','bias','starttime','scanspeed','intelmode','bit2nm','xoffset','yoffset','voidpixels')):
				create_bcr_header(line, header_dict)
	return(header_dict)



def read_bcr_bin(infilename):
	print("reading binary part (matrix) from bcr file")
	np.set_printoptions(threshold=np.inf)
	header_dict = read_bcr_header(infilename)
	if (('headersize' not in header_dict) or (header_dict['headersize'] == 2048)):
		header_size = 2048
	else:
		header_size = header_dict['headersize']			
	with open(infilename, mode = 'rb') as bcr_bin:
		bcr_bin.seek(header_size, os.SEEK_SET)
		bcr_array = np.fromfile(bcr_bin, dtype=np.int16)
		for i in range(0,len(bcr_array)):
			float(bcr_array[i])
		print(header_dict["xpixels"])
		print(header_dict["ypixels"])
		print(len(bcr_array))
		#bcr_array = header_dict["bit2nm"] * np.flipud(np.reshape(bcr_array, (header_dict["xpixels"], header_dict["ypixels"])))
		bcr_array = header_dict["bit2nm"] * (np.reshape(bcr_array, (header_dict["ypixels"], header_dict["xpixels"])))
		
	return(bcr_array)

#print(read_bcr_bin("../data/1012_1_crop_2.bcr"))

'''
def read_bcr_header(infilename):
	header_dict = {}
	with open(infilename, encoding='utf-8', errors='ignore') as bcr_file:
		line_num = 0
		for line in bcr_file:
			if (line.startswith(("#","%"))):
				continue # ignore comments
			if line.startswith('fileformat'):
				line_splitted = line.split(sep=" = ")
				bcr_param = line_splitted[0].strip() # parameter from bcr file
				bcr_value = line_splitted[1].strip() # value of that parameter
			if line.startswith(('headersize','xpixels','ypixels','xlength','ylength','current','bias','starttime','scanspeed','intelmode','bit2nm','xoffset','yoffset','voidpixels')):
				create_bcr_header(line, header_dict)
	print("Reading header part of bcr file")
	return(header_dict)


# ok, not a bin, but don't wanna rewrite all functions
def read_bcr_bin(infilename):
	bcr_array = np.genfromtxt(infilename, skip_header = 12)
	#highest_point = bcr_array.max() 
	#bcr_array = bcr_array + (1000 - highest_point) #put those 3 lines also in real read bcr bin function
	print("reading binary part (matrix) from bcr file")
	return(bcr_array)
'''
#read_bcr functions commented out because I need testing function
