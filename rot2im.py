#!/usr/bin/env python3

from read_pdb import read_pdb
from read_bcr_python import read_bcr_header
from pdb_bins import pdb_to_bins
import draw_plot
from transform_coordinates import rotate
import argparse

import linecache
import operator
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


def draw_points(matrix, bin_size, pdb_file_name, bcr_file_name):
	plt.switch_backend('TkAgg') #default backend is 'agg' and it can only draw png file. I use 'Qt4Agg' for interactive 3D graph. 
	
	fig, ax = plt.subplots()

	data = matrix
	
	highest = np.amax(matrix)
	lowest = np.amin(matrix)

	cax = ax.imshow(data, interpolation='nearest', cmap=cm.afmhot)
	ax.set_xlabel("px \n 1 px = {0:.3f}nm".format(bin_size))
	ax.set_ylabel("px")

	cbar = fig.colorbar(cax, ticks=[lowest,highest], orientation='horizontal')
	cbar.ax.set_xticklabels(["{0:.3f}nm".format(lowest),"{0:.3f}nm".format(highest)])  # horizontal colorbar

	graph = pdb_file_name.split(".")[0] + bcr_file_name.split(".")[0] + ".png"

	plt.savefig("snaduzok.png")
	plt.close()
	#plt.show()
	return(0)

def Main():
	#plt.switch_backend('Qt4Agg') 
	pdb = {}
	parser = argparse.ArgumentParser(description='Rotation from Docker output file to graph')
	parser.add_argument("pdb_file", help = "pdb file to read", type=str)
	parser.add_argument("bcr_file", help = "bcr file to read bin size", type=str)
	parser.add_argument("output_text", help = "<name of project>_textfile.txt", type=str) 
	parser.add_argument("line", help = "number of line to read axisangle", type=str)
	args = parser.parse_args()
		
	header = read_bcr_header(args.bcr_file)
	
	bin_size = header['xlength']/header['xpixels']

	pdb_lst = read_pdb(args.pdb_file)[1]
	#with open(args.output_text) as output:
	axisangle_line = linecache.getline(args.output_text, int(args.line))
	axisangle = operator.itemgetter(3,4,5,7)(axisangle_line.split())
	axisangle = list(axisangle)
	for i in range(0, len(axisangle)):
		axisangle[i] = float(axisangle[i])
	new_coors = rotate(axisangle,pdb_lst)
	#print(new_coors)
	#print(bin_size)
	bin_matrix = pdb_to_bins(bin_size,*new_coors)[0]
	np_bin_matrix = np.rot90(np.array(bin_matrix))
	#print(np_bin_matrix)
	draw_points(np_bin_matrix, bin_size, args.pdb_file, args.bcr_file)
	return()
if __name__  == '__main__' :
            Main()
