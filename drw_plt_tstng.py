import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from matplotlib import cm
#from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.ticker as tkr
import numpy as np
from pdb_bins import pdb_to_bins
import os
import pathlib
import pylab
def draw_points_test(diff_matrix,name):
    font = {'size':15}
    matplotlib.rc('font', **font)

    plt.switch_backend('agg') #default backend is 'agg' and it can only draw png file. I use 'Qt4Agg' for interactive 3D graph. 

    fig, (ax) = plt.subplots(ncols=1, figsize=(15,15))

    data = diff_matrix


    img1 = ax.imshow(data, cmap='afmhot')
    divider = make_axes_locatable(ax)
    cax1 = divider.append_axes("right", size="10%", pad=0.05)
    fig.colorbar(img1, cax=cax1, label="nm")

    ax.set_title('test')

    ax.set_xlabel("nm",labelpad=0.005)
    ax.set_ylabel("nm",labelpad=0.005)

    plt.tight_layout(h_pad=1)

    plt.savefig(name, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    #plt.show()
    return(0)


