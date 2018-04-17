import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import os
import cv2
import sys
from pdb_bins import pdb_to_bins
from read_pdb import read_pdb
pdb_list = read_pdb(sys.argv[1])[1]
pdb_in_bins = pdb_to_bins(float(sys.argv[2]),*pdb_list)[0]

def draw_points(diff_matrix):
    plt.switch_backend('agg') #default backend is 'agg' and it can only draw png file. I use 'Qt4Agg' for interactive 3D graph. 
    fig, (ax1) = plt.subplots(ncols=1)

    data = diff_matrix

    img1 = ax1.imshow(data, cmap='afmhot')
    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(img1, cax=cax1)

    ax1.set_title('Test matrices')
    ax1.set_xlabel("px")
    ax1.set_ylabel("px")

    plt.tight_layout(h_pad=1)

    plt.savefig("graph.png")
    plt.close()
    return(0)

draw_points(pdb_in_bins)
