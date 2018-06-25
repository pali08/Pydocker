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
def draw_points(diff_matrix, num_of_graph, subfolder, score, bin_size, pdb_aligned_matrix, bcr_matrix, rmsd):
    font = {'size':15}
    matplotlib.rc('font', **font)

    def format_func(value, tick_number):
        # find value
        tickval = "{:.1f}".format(value*bin_size)
        return(tickval)

    plt.switch_backend('agg') #default backend is 'agg' and it can only draw png file. I use 'Qt4Agg' for interactive 3D graph. 

    fig, (ax3, ax2, ax1) = plt.subplots(ncols=3, figsize=(15,15))

    data = diff_matrix
    data2 = pdb_aligned_matrix
    data3 = bcr_matrix

    maxval = max(diff_matrix.max(),pdb_aligned_matrix.max(),bcr_matrix.max())
    minval = min(diff_matrix.min(),pdb_aligned_matrix.min(),bcr_matrix.min())
    #fig.suptitle('Correlation score is {0:.3f}'.format(score), verticalalignment='bottom', pad=0.1, fontsize = 20)

    z_ticks = np.arange(minval,maxval+1,(maxval-minval)/4)

    img1 = ax1.imshow(data, cmap='afmhot', vmin=minval, vmax=maxval)
    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="10%", pad=0.05)
    fig.colorbar(img1, cax=cax1, label="nm", ticks=z_ticks)

    img3 = ax3.imshow(data3, cmap='afmhot', vmin=minval, vmax=maxval)
    divider = make_axes_locatable(ax3)
    cax3 = divider.append_axes("right", size="10%", pad=0.05)
    fig.colorbar(img3, cax=cax3, label="nm", ticks=z_ticks)


    img2 = ax2.imshow(data2, cmap='afmhot', vmin=minval,vmax=maxval)
    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="10%", pad=0.05)
    fig.colorbar(img2, cax=cax2, label="nm", ticks=z_ticks)

    if rmsd==True:
        score_type = "RMSD"
    else:
        score_type = "MAE"

    ax1.set_title('Subtracted surfaces')
    ax2.set_title('{1} score is {0:.3f}\n\nPDB surface'.format(score,score_type))
    ax3.set_title('AFM surface')

    ax1.set_xlabel("nm",labelpad=0.005)
    ax1.set_ylabel("nm",labelpad=0.005)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax1.set_xticks(np.arange(0, diff_matrix.shape[1]+1, diff_matrix.shape[1]/4))
    ax1.set_yticks(np.arange(0, diff_matrix.shape[0]+1, diff_matrix.shape[0]/4))

    #print(diff_matrix.shape[1])
    #print(diff_matrix.shape[0])

    ax2.set_xlabel("nm",labelpad=0.005)
    ax2.set_ylabel("nm",labelpad=0.005)
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax2.set_xticks(np.arange(0, data2.shape[1]+1, data2.shape[1]/4))
    ax2.set_yticks(np.arange(0, data2.shape[0]+1, data2.shape[0]/4))

    ax3.set_xlabel("nm",labelpad=0.005)
    ax3.set_ylabel("nm",labelpad=0.005)
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax3.set_xticks(np.arange(0, data3.shape[1]+1, data3.shape[1]/4))
    ax3.set_yticks(np.arange(0, data3.shape[0]+1, data3.shape[0]/4))

    plt.tight_layout(h_pad=1)

    graph = str(pathlib.Path(subfolder, "graph_{:02d}.png".format(num_of_graph+1)))
    plt.savefig(graph, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    #plt.show()
    return(0)

# TODO: picture name and folder in argument or by joining name of bcr and pdb files

